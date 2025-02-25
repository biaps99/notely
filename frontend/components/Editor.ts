import * as utils from '../utils';
import * as dom from '../dom';
import * as events from '../events';
import * as api from '../api';
import * as types from '../types';

const toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'],
  ['code-block'],
  ['link', 'image', 'formula'],
  [{ list: 'ordered' }, { list: 'bullet' }, { list: 'check' }],
  [{ script: 'sub' }, { script: 'super' }],
  [{ indent: '-1' }, { indent: '+1' }],
  [{ header: [1, 2, 3, 4, 5, 6, false] }],
  [{ font: [] }],
  [{ align: [] }],
];
const historyDelayInMilliseconds = 1000;

/**
 * Creates and manages the editor component.
 *
 * @param container - The container element where the editor should be appended.
 * @returns The created editor element.
 */
export const Editor = (container: HTMLElement) => {
  const editor = dom.createDivElement('editor');
  const editorContent = dom.createDivElement('editor__content', '');
  editorContent.setAttribute('id', 'quill-editor');
  editor.appendChild(editorContent);
  container.appendChild(editor);

  const quill = new Quill('#quill-editor', {
    theme: 'snow',
    modules: {
      toolbar: toolbarOptions,
      history: {
        delay: historyDelayInMilliseconds,
        userOnly: true,
      },
      imageDrop: true,
    },
  });

  let selectedNote: types.Note | null = null;

  events.addEventListener(events.SELECTED_NOTE, (e) => {
    selectedNote = e.detail;
    quill.root.innerHTML = selectedNote.content;
  });

  const updateDelayInMilliseconds = 1000;
  const updateNoteContent = utils.debounce(async () => {
    if (selectedNote) {
      const updatedContent = quill.root.innerHTML;
      selectedNote.content = updatedContent;
      await api.updateNote(
        selectedNote,
        selectedNote.id,
        selectedNote.folder_id
      );
    }
  }, updateDelayInMilliseconds);

  quill.on('text-change', updateNoteContent);

  return editor;
};
