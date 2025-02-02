const _eventTarget = new EventTarget();

/**
 * Adds an event listener for a specified event name.
 *
 * @param eventName - The name of the event to listen for.
 * @param listener - The callback function to be called when the event is triggered.
 *                   The function will receive the event as an argument.
 *
 * @example
 * addEventListener('fetchedFolders', (e) => { console.log(e.detail); });
 */
export const addEventListener = (
  eventName: string,
  listener: (e: CustomEvent) => void
): void => {
  _eventTarget.addEventListener(eventName, listener);
};

/**
 * Removes an event listener for a specified event name.
 *
 * @param eventName - The name of the event to stop listening for.
 * @param listener - The callback function that was previously added as an event listener.
 *
 * @example
 * removeEventListener('fetchedFolders', listener);
 */
export const removeEventListener = (
  eventName: string,
  listener: (e: CustomEvent) => void
): void => {
  _eventTarget.removeEventListener(eventName, listener);
};

/**
 * Dispatches a custom event with a specified event name and detail.
 *
 * @param eventName - The name of the event to dispatch.
 * @param detail - The data to be included with the event.
 *
 * @example
 * dispatchEvent('fetchedFolders', { folders: [] });
 */
export const dispatchEvent = (eventName: string, detail: any): void => {
  const event = new CustomEvent(eventName, { detail });
  _eventTarget.dispatchEvent(event);
};

export const FETCHED_FOLDERS = 'fetchedFolders';
export const UPDATED_FOLDER = 'updatedFolder';
export const CREATED_FOLDER = 'createdFolder';
