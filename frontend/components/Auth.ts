import { auth } from '../auth';
import * as dom from '../dom';

export const Login = (root: HTMLElement) => {
  const container = dom.createDivElement('login-container');
  const contentWrapper = dom.createDivElement('content-wrapper');

  const heading = dom.createDivElement(
    'heading',
    'Welcome to Notely. Your notes, organized.'
  );
  contentWrapper.appendChild(heading);

  container.appendChild(contentWrapper);
  root.appendChild(container);

  auth.addAuthContainer(contentWrapper);
};

export const Logout = (root: HTMLElement) => {
  const logoutBtn = dom.createButtonElement('logout-btn', 'Logout');
  logoutBtn.addEventListener('click', () => {
    auth.signOut();
  });
  root.appendChild(logoutBtn);
};
