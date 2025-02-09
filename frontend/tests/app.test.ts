import * as app from '../app';
import * as types from '../types';
import * as events from '../events';

describe('App Functions', () => {
  let api: any;
  let auth: any;
  let root: HTMLElement;
  let queue: any[];

  class TestAPI {
    async fetchFolders(): Promise<types.Folder[]> {
      return [
        {
          id: '1',
          name: 'Test Folder',
          isExpanded: false,
        },
      ];
    }
  }

  class TestAuth {
    onAuthStateChanged(callback: (user: any) => void) {
      callback({ uid: '123', displayName: 'Test User' });
    }

    login() {
      this.onAuthStateChanged((user) => user);
    }
  }

  beforeEach(() => {
    api = new TestAPI();
    auth = new TestAuth();
    root = document.createElement('div');
    queue = [];
    auth.login();
  });

  test('render updates folders when at least one', async () => {
    const updateListener = (e: CustomEvent) => {
      queue.push(1);
    };
    events.addEventListener(events.FETCHED_FOLDERS, updateListener);

    await app.render(root, api, auth);

    expect(queue).toHaveLength(1);
    expect(queue[0]).toEqual(1);

    events.removeEventListener(events.FETCHED_FOLDERS, updateListener);
  });

  test('render does not update folders when none', async () => {
    class EmptyAPI {
      async fetchFolders(): Promise<types.Folder[]> {
        return [];
      }
    }

    const updateListener = (e: CustomEvent) => {
      queue.push(1);
    };
    events.addEventListener(events.FETCHED_FOLDERS, updateListener);

    await app.render(root, new EmptyAPI(), auth);

    expect(queue).toHaveLength(0);

    events.removeEventListener(events.FETCHED_FOLDERS, updateListener);
  });

  test('render handles empty folders gracefully', async () => {
    class EmptyAPI {
      async fetchFolders(): Promise<types.Folder[]> {
        return [];
      }
    }

    await app.render(root, new EmptyAPI(), auth);

    expect(root.querySelector('.sidebar')).not.toBeNull();
  });

  test('render handles API errors gracefully', async () => {
    class ErrorAPI {
      async fetchFolders(): Promise<types.Folder[]> {
        throw new Error('API Error');
      }
    }

    await app.render(root, new ErrorAPI(), auth);

    expect(root.querySelector('.sidebar')).not.toBeNull();
  });
});
