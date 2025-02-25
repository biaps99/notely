import * as components from './components';
import * as defaultApi from './api';
import * as events from './events';
import { auth as defaultAuth } from './auth';

/**
 * Fetches folders from the API and initializes the sidebar.
 * @param api - The API to use for fetching data.
 */
const fetchFolders = async (api = defaultApi) => {
  try {
    const folders = await api.fetchFolders();
    if (folders.length > 0) {
      events.dispatchEvent(events.FETCHED_FOLDERS, folders);
    }
  } catch (error) {
    // TODO: Show an error message in the UI
  }
};

/**
 * Main render function for the application.
 * @param root - The root element to render the app into.
 * @param api - The API to use for fetching data.
 * @param auth - The authentication service to use.
 */
export const render = (
  root: HTMLElement,
  api = defaultApi,
  auth = defaultAuth
) => {
  auth.onAuthStateChanged((user) => {
    root.innerHTML = '';
    if (user) {
      const sidebar = components.Sidebar(root, []);
      events.addEventListener(events.FETCHED_FOLDERS, (e) => {
        root.removeChild(sidebar);
        components.Sidebar(root, e.detail);
        components.Editor(root);
      });

      components.Logout(root);

      fetchFolders(api);
    } else {
      components.Login(root);
    }
  });
};
