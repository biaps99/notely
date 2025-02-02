import * as app from '../app';
import * as types from '../types';
import * as events from '../events';

describe('App Functions', () => {
  test('render fetches folders', () => {
    const folders = [
      {
        id: '1',
        notes: [
          {
            id: '1',
            content: 'Test Note',
            title: 'Test Note',
            folder_id: '1',
            updated_at: '2021-01-01',
          },
        ],
        name: 'Test Folder',
        isExpanded: false,
      },
    ];

    let queue = [];

    class TestAPI {
      async fetchFolders(): Promise<types.Folder[]> {
        queue.push(folders);
        return folders;
      }
    }

    app.render(document.createElement('div'), new TestAPI());

    expect(queue).toHaveLength(1);
    expect(queue[0]).toEqual(folders);
  });

  test('render updates folders when at least one', async () => {
    let queue = [];

    class TestAPI {
      async fetchFolders(): Promise<types.Folder[]> {
        return [
          {
            id: '1',
            notes: [],
            name: 'Test Folder',
            isExpanded: false,
          },
        ];
      }
    }

    const updateListener = (e: CustomEvent) => {
      queue.push(1);
    };

    events.addEventListener(events.FETCHED_FOLDERS, updateListener);

    await app.render(document.createElement('div'), new TestAPI());

    expect(queue).toHaveLength(1);
    expect(queue[0]).toEqual(1);
  });

  test('render does not update folders when none', async () => {
    let queue = [];

    class TestAPI {
      async fetchFolders(): Promise<types.Folder[]> {
        return [];
      }
    }

    const updateListener = (e: CustomEvent) => {
      queue.push(1);
    };

    events.addEventListener(events.UPDATE_FOLDERS, updateListener);

    await app.render(document.createElement('div'), new TestAPI());

    expect(queue).toHaveLength(0);
  });

  test('render handles empty folders gracefully', () => {
    class TestAPI {
      async fetchFolders(): Promise<types.Folder[]> {
        return [];
      }
    }

    let root = document.createElement('div');
    app.render(root, new TestAPI());

    expect(root.querySelector('.sidebar')).not.toBeNull();
  });

  test('render handles API errors gracefully', async () => {
    class TestAPI {
      async fetchFolders(): Promise<types.Folder[]> {
        throw new Error('API Error');
      }
    }

    let root = document.createElement('div');
    app.render(root, new TestAPI());

    expect(root.querySelector('.sidebar')).not.toBeNull();
  });
});
