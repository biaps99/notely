import * as dom from '../dom';

export const auth = {
  addAuthContainer: (root: HTMLElement) => {
    root.appendChild(dom.createDivElement('fake-auth-container'));
  },
  signOut: async () => Promise.resolve(),
  onAuthStateChanged: (callback: (user: null) => void) => {
    callback(null);
  },
  getToken: async (): Promise<string | null> => {
    return Promise.resolve(null);
  },
};
