import * as types from '../types';
import * as dom from '../dom';
import * as defaultApi from '../api';
import * as utils from '../utils';

/**
 * Creates and manages the sidebar.
 * @param container - The container element to render the sidebar into.
 * @param folders - The list of folders to display in the sidebar.
 * @param api - The API object to interact with the backend.
 * @returns The sidebar element.
 */
export const Sidebar = (
  container: HTMLElement,
  folders: types.Folder[],
  api: typeof defaultApi = defaultApi
) => {
  const sidebar = dom.createDivElement('sidebar');
  sidebar.append(
    createAddFolderButton(api, sidebar),
    createFolderList(folders, api, sidebar)
  );
  container.appendChild(sidebar);
  return sidebar;
};

/**
 * Creates a folder button and event listener.
 * @param api - The API object to interact with the backend.
 * @param sidebar - The sidebar element for localized queries.
 * @returns The add folder button element.
 */
const createAddFolderButton = (
  api: typeof defaultApi,
  sidebar: HTMLElement
): HTMLButtonElement => {
  const button = dom.createButtonElement('sidebar__add_folder', 'New Folder');
  button.addEventListener('click', () =>
    addNewFolder(
      { name: 'New Folder', isExpanded: false, id: '' },
      api,
      sidebar
    )
  );
  return button;
};

/**
 * Creates the list of folders for the sidebar.
 * @param folders - The folders to display.
 * @param api - The API object.
 * @param sidebar - The sidebar element for localized queries.
 * @returns The folder list element.
 */
const createFolderList = (
  folders: types.Folder[],
  api: typeof defaultApi,
  sidebar: HTMLElement
): HTMLElement => {
  const folderList = dom.createDivElement('sidebar__folder_list');
  folders.forEach((folder) =>
    folderList.appendChild(createFolderItem(folder, api, sidebar))
  );
  return folderList;
};

/**
 * Creates a folder item element.
 * @param folder - The folder to create.
 * @param api - The API object.
 * @param sidebar - The sidebar element for localized queries.
 * @returns The folder item element.
 */
const createFolderItem = (
  folder: types.Folder,
  api: typeof defaultApi,
  sidebar: HTMLElement
): HTMLElement => {
  const folderItem = dom.createDivElement('sidebar__folder_item');
  const header = dom.createDivElement('sidebar__folder_header');

  header.append(
    createEditableFolderName(folder, api),
    createOptionsButton(folder, api, folderItem),
    createCollapseButton(folder, folderItem, api, sidebar)
  );
  folderItem.appendChild(header);

  return folderItem;
};

/**
 * Creates an editable folder name element.
 * @param folder - The folder to display.
 * @param api - The API object.
 * @returns The folder name element.
 */
const createEditableFolderName = (
  folder: types.Folder,
  api: typeof defaultApi
): HTMLElement => {
  const folderName = dom.createDivElement('sidebar__folder_name', folder.name);
  folderName.addEventListener('click', () => {
    const input = dom.createInputElement(
      'sidebar__folder_name_input',
      'text',
      folder.name
    );
    input.addEventListener('blur', () => input.replaceWith(folderName));
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        changeFolderName(folder, input, folderName, api);
      }
    });
    folderName.replaceWith(input);
    input.focus();
    input.select();
  });
  return folderName;
};

/**
 * Changes the folder name.
 * @param folder - The folder to change the name of.
 * @param input - The input element containing the new name.
 * @param folderName - The folder name element to replace.
 * @param api - The API object.
 */
const changeFolderName = async (
  folder: types.Folder,
  input: HTMLInputElement,
  folderName: HTMLElement,
  api: typeof defaultApi
) => {
  const updatedName = input.value.trim();
  if (updatedName !== folder.name) {
    const oldName = folder.name;
    folder.name = updatedName;
    folderName.textContent = updatedName;
    try {
      await api.updateFolder({ name: folder.name }, folder.id);
    } catch {
      folder.name = oldName;
      folderName.textContent = folder.name;
    }
  }
  input.replaceWith(folderName);
};

/**
 * Changes the note title.
 * @param note - The note to change the title of.
 * @param input - The input element containing the new title.
 * @param noteTitle - The note title element to replace.
 * @param api - The API object.
 */
const changeNoteTitle = async (
  note: types.Note,
  input: HTMLInputElement,
  noteTitle: HTMLElement,
  api: typeof defaultApi,
  noteItem: HTMLElement
) => {
  const updatedTitle = input.value.trim();
  if (updatedTitle !== note.title) {
    const oldTitle = note.title;
    try {
      const updatedNote = await api.updateNote(
        { title: updatedTitle },
        note.id,
        note.folder_id
      );
      note.last_updated_at = updatedNote.last_updated_at;
      note.title = updatedNote.title;
      noteTitle.textContent = updatedNote.title;
      const noteLastUpdatedAt = dom.queryElement(
        noteItem,
        '.sidebar__note_last_updated_at'
      );
      noteLastUpdatedAt.textContent = utils.formatDate(
        updatedNote.last_updated_at
      );
    } catch {
      note.title = oldTitle;
      noteTitle.textContent = note.title;
    }
  }
  input.replaceWith(noteTitle);
};

/**
 * Creates the collapse/expand button for a folder.
 * @param folder - The folder to collapse/expand.
 * @param folderItem - The folder element.
 * @param api - The API object.
 * @param sidebar - The sidebar element for localized queries.
 * @returns The collapse/expand button element.
 */
const createCollapseButton = (
  folder: types.Folder,
  folderItem: HTMLElement,
  api: typeof defaultApi,
  sidebar: HTMLElement
): HTMLButtonElement => {
  const button = dom.createButtonElement(
    'sidebar__folder_collapse',
    folder.isExpanded ? '-' : '+'
  );
  button.addEventListener('click', () => {
    if (folder.isExpanded) {
      collapseFolder(folder, folderItem);
      button.textContent = '+';
    } else {
      expandFolder(folder, folderItem, api, sidebar);
      button.textContent = '-';
    }
  });
  return button;
};

/**
 * Expands the folder and loads notes.
 * @param folder - The folder to expand.
 * @param folderItem - The folder item element.
 * @param api - The API object.
 * @param sidebar - The sidebar element for localized queries.
 */
const expandFolder = (
  folder: types.Folder,
  folderItem: HTMLElement,
  api: typeof defaultApi,
  sidebar: HTMLElement
): void => {
  showFolderNotes(folder.id, folderItem, api, sidebar);
  folder.isExpanded = true;
};

/**
 * Collapses the folder and removes notes.
 * @param folder - The folder to collapse.
 * @param folderItem - The folder item element.
 */
const collapseFolder = (
  folder: types.Folder,
  folderItem: HTMLElement
): void => {
  const noteList = dom.queryElement(folderItem, '.sidebar__note_list');
  noteList?.remove();
  folder.isExpanded = false;
};

/**
 * Shows notes for a folder.
 * @param folderId - The folder ID.
 * @param folderItem - The folder item element.
 * @param api - The API object.
 * @param sidebar - The sidebar element for localized queries.
 */
const showFolderNotes = async (
  folderId: string,
  folderItem: HTMLElement,
  api: typeof defaultApi,
  sidebar: HTMLElement
): Promise<void> => {
  try {
    const notes = await api.fetchFolderNotes(folderId);
    folderItem.appendChild(createNoteList(notes, sidebar, api));
    if (notes.length > 0) selectNote(notes[0], sidebar);
  } catch (error) {
    // TODO: Handle error
    throw error;
  }
};

/**
 * Creates the list of notes for a folder.
 * @param notes - The list of notes.
 * @param sidebar - The sidebar element for localized queries.
 * @param api - The API object.
 * @returns The note list element.
 */
const createNoteList = (
  notes: types.Note[],
  sidebar: HTMLElement,
  api: typeof defaultApi
): HTMLElement => {
  const noteList = dom.createDivElement('sidebar__note_list');
  notes.forEach((note) =>
    noteList.appendChild(createNoteItem(note, sidebar, api))
  );
  return noteList;
};

/**
 * Creates a note item element.
 * @param note - The note to create.
 * @param sidebar - The sidebar element for localized queries.
 * @param api - The API object.
 * @returns The note item element.
 */
const createNoteItem = (
  note: types.Note,
  sidebar: HTMLElement,
  api: typeof defaultApi
): HTMLElement => {
  const noteItem = dom.createDivElement('sidebar__note_item');
  noteItem.id = `note-item-${note.id}`;

  const deleteButton = dom.createButtonElement('sidebar__delete_note', 'x');
  deleteButton.addEventListener('click', () => {
    const confirmDelete = window.confirm(
      `Are you sure you want to delete the note ${note.title}?`
    );
    if (confirmDelete) deleteNote(note.id, note.folder_id, noteItem, api);
  });

  const noteDetails = dom.createDivElement('sidebar__note_details');
  noteDetails.append(
    createEditableNoteTitle(note, api, noteItem),
    dom.createDivElement(
      'sidebar__note_last_updated_at',
      utils.formatDate(note.last_updated_at)
    )
  );

  noteItem.append(noteDetails, deleteButton);
  noteItem.addEventListener('click', () => selectNote(note, sidebar));
  return noteItem;
};

/**
 * Selects a note and highlights it.
 * @param note - The selected note.
 * @param sidebar - The sidebar element for localized queries.
 */
const selectNote = (note: types.Note, sidebar: HTMLElement): void => {
  const selectedNote = dom.queryElement(
    sidebar,
    '.sidebar__note_item--selected'
  );
  const nextNote = dom.queryElement(sidebar, `#note-item-${note.id}`);
  selectedNote?.classList.remove('sidebar__note_item--selected');
  nextNote?.classList.add('sidebar__note_item--selected');
};

/**
 * Adds a new folder to the sidebar.
 * @param folder - The folder to add.
 * @param api - The API object.
 * @param sidebar - The sidebar element for localized queries.
 */
const addNewFolder = async (
  folder: types.Folder,
  api: typeof defaultApi,
  sidebar: HTMLElement
) => {
  try {
    const newFolder = await api.createFolder(folder);
    const folderList = dom.queryElement(sidebar, '.sidebar__folder_list');
    const newFolderItem = createFolderItem(newFolder, api, sidebar);
    folderList.appendChild(newFolderItem);
    const folderName = dom.queryElement(
      newFolderItem,
      '.sidebar__folder_name'
    ) as HTMLElement;
    folderName.click();
  } catch (error) {
    // TODO: Handle error
    throw error;
  }
};

/**
 * Creates an editable note title element.
 * @param note - The note to display.
 * @param api - The API object.
 * @returns The note title element.
 */
const createEditableNoteTitle = (
  note: types.Note,
  api: typeof defaultApi,
  noteItem: HTMLElement
): HTMLElement => {
  const noteTitle = dom.createDivElement('sidebar__note_title', note.title);
  noteTitle.addEventListener('click', () => {
    const input = dom.createInputElement(
      'sidebar__note_title_input',
      'text',
      note.title
    );
    input.addEventListener('blur', () => input.replaceWith(noteTitle));
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        changeNoteTitle(note, input, noteTitle, api, noteItem);
      }
    });
    noteTitle.replaceWith(input);
    input.focus();
    input.select();
  });
  return noteTitle;
};

/**
 * Deletes a note from the sidebar.
 * @param noteId - The ID of the note to delete.
 * @param folderId - The ID of the folder that contains the note.
 * @param sidebar - The sidebar element for localized queries.
 * @param api - The API object.
 * @returns A promise that resolves when the note is deleted.
 */
const deleteNote = async (
  noteId: string,
  folderId: string,
  noteItem: HTMLElement,
  api: typeof defaultApi
) => {
  try {
    await api.deleteNote(noteId, folderId);
    noteItem.remove();
  } catch (error) {
    // TODO: Handle error
    throw error;
  }
};

/**
 * Creates an options button with a dropdown menu for "Delete Folder" and "Add Note".
 * @param folder - The folder to perform actions on.
 * @param api - The API object.
 * @param folderItem - The folder item element.
 * @returns The options button element.
 */
const createOptionsButton = (
  folder: types.Folder,
  api: typeof defaultApi,
  folderItem: HTMLElement
): HTMLButtonElement => {
  const optionsButton = dom.createButtonElement(
    'sidebar__folder_options_button',
    '...'
  );
  const dropdownMenu = dom.createDivElement('sidebar__folder_dropdown_menu');

  const addNoteOption = dom.createDivElement(
    'sidebar__folder_dropdown_option',
    'Add Note'
  );
  addNoteOption.addEventListener('click', () => {
    addNewNote(folder, api, folderItem);
  });

  const deleteFolderOption = dom.createDivElement(
    'sidebar__folder_dropdown_option',
    'Delete Folder'
  );
  deleteFolderOption.addEventListener('click', () => {
    const confirmDelete = window.confirm(
      `Are you sure you want to delete the folder "${folder.name}"?`
    );
    if (confirmDelete) {
      deleteFolder(folder.id, folderItem, api);
    }
  });

  dropdownMenu.append(addNoteOption, deleteFolderOption);
  optionsButton.appendChild(dropdownMenu);

  optionsButton.addEventListener('click', (e) => {
    e.stopPropagation();
    const isVisible = dropdownMenu.style.display === 'block';
    dropdownMenu.style.display = isVisible ? 'none' : 'block';
  });

  document.addEventListener('click', (e) => {
    if (!optionsButton.contains(e.target as Node)) {
      dropdownMenu.style.display = 'none';
    }
  });

  return optionsButton;
};

/**
 * Adds a new note to the specified folder.
 * @param folderId - The ID of the folder to add a note to.
 * @param api - The API object.
 * @param folderItem - The folder item element to append the new note to.
 */
const addNewNote = async (
  folder: types.Folder,
  api: typeof defaultApi,
  folderItem: HTMLElement
) => {
  try {
    if (!folder.isExpanded) {
      const expandFolderButton = dom.queryElement(
        folderItem,
        '.sidebar__folder_collapse'
      ) as HTMLElement;
      expandFolderButton.click();
    }
    const newNote = await api.createNote(
      {
        title: 'New Note',
      },
      folder.id
    );
    const noteList = dom.queryElement(folderItem, '.sidebar__note_list');
    const newNoteItem = createNoteItem(
      newNote,
      folderItem.parentElement as HTMLElement,
      api
    );
    noteList?.appendChild(newNoteItem);
    const newNoteTitle = dom.queryElement(
      newNoteItem as HTMLElement,
      '.sidebar__note_title'
    ) as HTMLElement;
    newNoteTitle.click();
  } catch (error) {
    // TODO: Handle error
    throw error;
  }
};

/**
 * Deletes a folder from the sidebar.
 * @param folderId - The ID of the folder to delete.
 * @param folderItem - The folder item element to remove.
 * @param api - The API object.
 */
const deleteFolder = async (
  folderId: string,
  folderItem: HTMLElement,
  api: typeof defaultApi
) => {
  try {
    await api.deleteFolder(folderId);
    folderItem.remove();
  } catch (error) {
    // TODO: Handle error
    throw error;
  }
};
