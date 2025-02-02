/**
 * Queries an element within a container based on a selector.
 * @param container - The container to query within.
 * @param selector - The selector to query for.
 * @returns The element if found, otherwise null.
 */
export const queryElement = (
  container: HTMLElement,
  selector: string
): Element | null => container.querySelector(selector);

/**
 * Creates a div element with a class and optional text content.
 * @param className - The class name to apply to the div.
 * @param text - Optional text content for the div (default is an empty string).
 * @returns The created div element.
 */
export const createDivElement = (
  className: string,
  text: string = ''
): HTMLDivElement => {
  const div = document.createElement('div');
  div.classList.add(className);
  if (text) div.textContent = text;
  return div;
};

/**
 * Creates a button element with a class and optional text content.
 * @param className - The class name to apply to the button.
 * @param text - Optional text content for the button (default is an empty string).
 * @returns The created button element.
 */
export const createButtonElement = (
  className: string,
  text: string = ''
): HTMLButtonElement => {
  const button = document.createElement('button');
  button.classList.add(className);
  button.type = 'button';
  if (text) button.textContent = text;
  return button;
};

/**
 * Creates an input element with a class, type, value, and placeholder.
 * @param className - The class name to apply to the input.
 * @param type - The type of the input element (default is 'text').
 * @param value - The initial value of the input element (default is an empty string).
 * @param placeholder - The placeholder text for the input (default is an empty string).
 * @returns The created input element.
 */
export const createInputElement = (
  className: string,
  type: string = 'text',
  value: string = '',
  placeholder: string = ''
): HTMLInputElement => {
  const input = document.createElement('input');
  input.classList.add(className);
  input.type = type;
  input.value = value;
  input.placeholder = placeholder;

  return input;
};
