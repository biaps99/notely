import { auth as firebaseAuth } from './firebase';
import { auth as fakeAuth } from './fake';

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

export const auth: Auth =
  process.env.NODE_ENV === 'testing' ? fakeAuth : firebaseAuth;
