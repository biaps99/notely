type User = {
  uid: string;
  name: string;
  email: string;
  getIdToken: () => Promise<string>;
};

type Auth = {
  addAuthContainer: (root: HTMLElement) => void;
  signOut: () => Promise<void>;
  onAuthStateChanged: (callback: (user: User) => void) => void;
  getToken: () => Promise<string | null>;
};

let auth: Auth;

if (process.env.NODE_ENV === 'test') {
  import('./fake').then((module) => {
    auth = module.auth;
  });
} else {
  import('./firebase').then((module) => {
    auth = module.auth;
  });
}

export { auth };
