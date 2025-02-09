import {
  signOut as firebaseSignOut,
  onAuthStateChanged as firebaseonAuthStateChanged,
} from 'firebase/auth';
import { initializeApp } from 'firebase/app';
import { getAuth, GithubAuthProvider } from 'firebase/auth';
import * as firebaseui from 'firebaseui';
import * as dom from '../dom';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

const app = initializeApp(firebaseConfig);

const appAuth = getAuth(app);

const ui = new firebaseui.auth.AuthUI(appAuth);

const uiConfig = {
  signInSuccessUrl: '/',
  signInOptions: [GithubAuthProvider.PROVIDER_ID],
  signInFlow: 'popup',
};

const addAuthContainer = (root: HTMLElement) => {
  const container = dom.createDivElement('firebaseui-auth-container');
  container.id = 'firebaseui-auth-container';
  root.appendChild(container);
  ui.start('#firebaseui-auth-container', uiConfig);
};

const signOut = async () => {
  await firebaseSignOut(appAuth);
};

const onAuthStateChanged = (callback: any) =>
  firebaseonAuthStateChanged(appAuth, callback);

const getToken = async (): Promise<string | null> => {
  const user = appAuth.currentUser;
  return user ? await user.getIdToken() : null;
};

export const auth = {
  addAuthContainer,
  signOut,
  onAuthStateChanged,
  getToken,
};
