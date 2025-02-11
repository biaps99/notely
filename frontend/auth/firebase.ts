import {
  signOut as firebaseSignOut,
  onAuthStateChanged as firebaseonAuthStateChanged,
} from 'firebase/auth';
import { initializeApp } from 'firebase/app';
import { getAuth, GithubAuthProvider } from 'firebase/auth';
import * as firebaseui from 'firebaseui';
import * as dom from '../dom';

let _app;
let _appAuth;
let _ui;

function getFirebaseConfig() {
  return {
    apiKey: process.env.FIREBASE_API_KEY,
    authDomain: process.env.FIREBASE_AUTH_DOMAIN,
    projectId: process.env.FIREBASE_PROJECT_ID,
    storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.FIREBASE_APP_ID,
  };
}

const getApp = () => {
  if (_app) return _app;
  _app = initializeApp(getFirebaseConfig());
  return _app;
};

const getAppAuth = () => {
  if (_appAuth) return _appAuth;
  _appAuth = getAuth(getApp());
  return _appAuth;
};

const getUi = () => {
  if (_ui) return _ui;
  _ui = new firebaseui.auth.AuthUI(getAppAuth());
  return _ui;
};

const uiConfig = {
  signInSuccessUrl: '/',
  signInOptions: [GithubAuthProvider.PROVIDER_ID],
  signInFlow: 'popup',
};

const addAuthContainer = (root: HTMLElement) => {
  const container = dom.createDivElement('firebaseui-auth-container');
  container.id = 'firebaseui-auth-container';
  root.appendChild(container);
  getUi().start('#firebaseui-auth-container', uiConfig);
};

const signOut = async () => {
  await firebaseSignOut(getAppAuth());
};

const onAuthStateChanged = (callback: any) =>
  firebaseonAuthStateChanged(getAppAuth(), callback);

const getToken = async (): Promise<string | null> => {
  const user = getAppAuth().currentUser;
  return user ? await user.getIdToken() : null;
};

export const auth = {
  addAuthContainer,
  signOut,
  onAuthStateChanged,
  getToken,
};
