import * as types from '../../types';
import { Sidebar } from '../../components';
import { formatDate } from '../../utils';

describe('Sidebar Component', () => {
  let container: HTMLElement;
  const folders = [
    {
      id: '1',
      name: 'Folder 1',
      isExpanded: false,
      notes: [
        {
          id: '1',
          content: 'Note 1',
          title: 'Note 1',
          folder_id: '1',
          last_updated_at: '121-01-01',
        },
        {
          id: '2',
          content: 'Note 2',
          title: 'Note 2',
          folder_id: '1',
          last_updated_at: '121-02-01',
        },
      ],
    },
    {
      id: '2',
      name: 'Folder 2',
      isExpanded: false,
      notes: [
        {
          id: '3',
          content: 'Note 3',
          title: 'Note 3',
          folder_id: '2',
          last_updated_at: '121-03-01',
        },
      ],
    },
  ];

  const fakeApi = {
    fetchFolderNotes: async (folderId: string) => {
      const folder = folders.find((f) => f.id === folderId);
      return folder ? folder.notes : [];
    },
    updateFolder: async (folder: Partial<types.Folder>, folderId: string) => {
      return folder;
    },
    createFolder: async (folder: types.Folder) => {
      folders.push(folder);
      return folder;
    },
    updateNote: async (note: Partial<types.Note>, noteId: string) => {
      return note;
    },
    deleteNote: async (noteId: string) => {
      return true;
    },
    deleteFolder: async (folderId: string) => {
      folders.splice(
        folders.findIndex((f) => f.id === folderId),
        1
      );
      return true;
    },
    createNote: async (note: types.Note) => {
      const folder = folders.find((f) => f.id === note.folder_id);
      if (folder) {
        folder.notes.push(note);
      }
      return note;
    },
  };

  beforeEach(() => {
    container = document.createElement('div');
    folders.forEach((folder) => (folder.isExpanded = false));
    Sidebar(container, folders, fakeApi);
  });

  test('renders the sidebar', () => {
    expect(container.querySelector('.sidebar')).not.toBeNull();
  });

  test('renders the "Add Folder" button', () => {
    expect(container.querySelector('.sidebar__add_folder')).not.toBeNull();
  });

  test('renders folder list with correct number of items', () => {
    const folderItems = container.querySelectorAll('.sidebar__folder_item');
    expect(folderItems.length).toBe(folders.length);
  });

  test('renders correct folder headers and collapse buttons', () => {
    const folderItems = container.querySelectorAll('.sidebar__folder_item');
    folderItems.forEach((folderItem, index) => {
      const folderName = folderItem.querySelector('.sidebar__folder_name');
      expect(folderName?.textContent).toBe(folders[index].name);

      const collapseButton = folderItem.querySelector(
        '.sidebar__folder_collapse'
      );
      expect(collapseButton).not.toBeNull();
      expect(collapseButton?.textContent).toBe('+');
    });
  });

  test('renders notes for expanded folder', async () => {
    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderCollapseButton = folderItem.querySelector(
      '.sidebar__folder_collapse'
    );
    folderCollapseButton?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    await new Promise((resolve) => setTimeout(resolve, 1));

    const noteList = folderItem.querySelector('.sidebar__note_list');
    expect(noteList).not.toBeNull();

    const noteItems = folderItem.querySelectorAll('.sidebar__note_item');
    folders[0].notes.forEach((note, index) => {
      const noteItem = noteItems[index];
      expect(noteItem.querySelector('.sidebar__note_title')?.textContent).toBe(
        note.title
      );
      expect(
        noteItem.querySelector('.sidebar__note_last_updated_at')?.textContent
      ).toBe(formatDate(note.last_updated_at));
    });
  });

  test('selects a note on click', async () => {
    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderCollapseButton = folderItem.querySelector(
      '.sidebar__folder_collapse'
    );
    folderCollapseButton?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    await new Promise((resolve) => setTimeout(resolve, 1));

    const noteItems = folderItem.querySelectorAll('.sidebar__note_item');
    const firstNote = noteItems[0];
    const secondNote = noteItems[1];

    firstNote.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    expect(firstNote.classList).toContain('sidebar__note_item--selected');
    expect(secondNote.classList).not.toContain('sidebar__note_item--selected');

    secondNote.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    expect(secondNote.classList).toContain('sidebar__note_item--selected');
    expect(firstNote.classList).not.toContain('sidebar__note_item--selected');
  });

  test('renders correctly with no folders', () => {
    container.innerHTML = '';
    Sidebar(container, []);
    const folderList = container.querySelector('.sidebar__folder_list');
    expect(folderList?.children.length).toBe(0);
  });

  test('allows editing folder name on click', async () => {
    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderName = folderItem.querySelector('.sidebar__folder_name');
    const newFolderName = 'Updated Folder Name';

    folderName?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    const input = folderItem.querySelector(
      'input[type="text"]'
    ) as HTMLInputElement;
    input.value = newFolderName;
    input.dispatchEvent(new Event('input', { bubbles: true }));

    input.dispatchEvent(
      new KeyboardEvent('keydown', { key: 'Enter', bubbles: true })
    );
    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(folderItem.querySelector('.sidebar__folder_name')?.textContent).toBe(
      newFolderName
    );
  });

  test('cancels folder name editing on blur', () => {
    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderName = folderItem.querySelector('.sidebar__folder_name');
    const originalName = folders[0].name;

    folderName?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    const input = folderItem.querySelector(
      'input[type="text"]'
    ) as HTMLInputElement;
    input.value = 'Changed Name';
    input.dispatchEvent(new Event('input', { bubbles: true }));

    input.dispatchEvent(new KeyboardEvent('blur', { bubbles: true }));

    expect(folderItem.querySelector('.sidebar__folder_name')?.textContent).toBe(
      originalName
    );
  });

  test('does not allow setting folder name to empty string', async () => {
    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderName = folderItem.querySelector('.sidebar__folder_name');

    folderName?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    const input = folderItem.querySelector(
      'input[type="text"]'
    ) as HTMLInputElement;
    input.value = '';
    input.dispatchEvent(new Event('input', { bubbles: true }));

    input.dispatchEvent(
      new KeyboardEvent('keydown', { key: 'Enter', bubbles: true })
    );
    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(folderItem.querySelector('.sidebar__folder_name')?.textContent).toBe(
      folders[0].name
    );
  });

  test('retains folder expanded/collapsed state after update', async () => {
    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const collapseButton = folderItem.querySelector(
      '.sidebar__folder_collapse'
    );

    collapseButton?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    expect(folders[0].isExpanded).toBe(true);

    collapseButton?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    expect(folders[0].isExpanded).toBe(false);
  });

  test('handles folder expand with no notes correctly', async () => {
    const emptyFolder = { id: '3', name: 'Empty Folder', isExpanded: false };
    container.innerHTML = '';
    Sidebar(container, [emptyFolder]);

    const folderItem = container.querySelector('.sidebar__folder_item');
    const folderCollapseButton = folderItem.querySelector(
      '.sidebar__folder_collapse'
    );
    folderCollapseButton?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    expect(folderItem.querySelector('.sidebar__note_list')).toBeNull();
  });

  test('expands and collapses folder note list', async () => {
    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderCollapseButton = folderItem.querySelector(
      '.sidebar__folder_collapse'
    );

    folderCollapseButton?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );
    await new Promise((resolve) => setTimeout(resolve, 1));
    expect(folderItem.querySelector('.sidebar__note_list')).not.toBeNull();

    folderCollapseButton?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );
    await new Promise((resolve) => setTimeout(resolve, 1));
    expect(folderItem.querySelector('.sidebar__note_list')).toBeNull();
  });

  test('creates a new folder and allows editing its name', async () => {
    const addButton = container.querySelector('.sidebar__add_folder');
    addButton?.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    await new Promise((resolve) => setTimeout(resolve, 1));

    const folderItems = container.querySelectorAll('.sidebar__folder_item');
    const newFolder = folderItems[folderItems.length - 1];
    const folderName = newFolder.querySelector('.sidebar__folder_name');
    const newFolderName = 'Updated Folder Name';

    folderName?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    const input = newFolder.querySelector(
      'input[type="text"]'
    ) as HTMLInputElement;
    input.value = newFolderName;
    input.dispatchEvent(new Event('input', { bubbles: true }));

    input.dispatchEvent(
      new KeyboardEvent('keydown', { key: 'Enter', bubbles: true })
    );
    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(newFolder.querySelector('.sidebar__folder_name')?.textContent).toBe(
      newFolderName
    );
  });

  test('allows editing note title on click', async () => {
    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderCollapseButton = folderItem.querySelector(
      '.sidebar__folder_collapse'
    );
    folderCollapseButton?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    await new Promise((resolve) => setTimeout(resolve, 1));

    const noteItem = container.querySelectorAll('.sidebar__note_item')[0];
    const noteTitle = noteItem.querySelector('.sidebar__note_title');
    const newNoteTitle = 'Updated Note Title';

    noteTitle?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    const input = noteItem.querySelector(
      'input[type="text"]'
    ) as HTMLInputElement;
    input.value = newNoteTitle;
    input.dispatchEvent(new Event('input', { bubbles: true }));

    input.dispatchEvent(
      new KeyboardEvent('keydown', { key: 'Enter', bubbles: true })
    );
    await new Promise((resolve) => setTimeout(resolve, 0));

    expect(noteItem.querySelector('.sidebar__note_title')?.textContent).toBe(
      newNoteTitle
    );
  });

  test('cancels note title editing on blur', async () => {
    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderCollapseButton = folderItem.querySelector(
      '.sidebar__folder_collapse'
    );
    folderCollapseButton?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    await new Promise((resolve) => setTimeout(resolve, 1));

    const noteItem = container.querySelectorAll('.sidebar__note_item')[0];
    const noteTitle = noteItem.querySelector('.sidebar__note_title');
    const newNoteTitle = 'Updated Note Title';
    const originalTitle = folders[0].notes[0].title;

    noteTitle?.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    const input = noteItem.querySelector(
      'input[type="text"]'
    ) as HTMLInputElement;
    input.value = newNoteTitle;
    input.dispatchEvent(new Event('input', { bubbles: true }));

    input.dispatchEvent(new KeyboardEvent('blur', { bubbles: true }));

    expect(noteItem.querySelector('.sidebar__note_title')?.textContent).toBe(
      originalTitle
    );
  });

  test('deletes a note after confirmation', async () => {
    const confirmSpy = jest.spyOn(window, 'confirm').mockImplementation(() => {
      return true;
    });

    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderCollapseButton = folderItem.querySelector(
      '.sidebar__folder_collapse'
    );
    folderCollapseButton?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    await new Promise((resolve) => setTimeout(resolve, 1));

    const noteItem = folderItem.querySelectorAll('.sidebar__note_item')[0];
    const deleteButton = noteItem.querySelector('.sidebar__delete_note');
    expect(deleteButton).not.toBeNull();

    deleteButton.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    await new Promise((resolve) => setTimeout(resolve, 1));

    expect(folderItem.querySelectorAll('.sidebar__note_item').length).toBe(1);
    expect(folderItem.querySelector(`#note-item-${noteItem.id}`)).toBeNull();

    expect(confirmSpy).toHaveBeenCalled();
    confirmSpy.mockRestore();
  });

  test('does not delete a note when canceled', async () => {
    const confirmSpy = jest.spyOn(window, 'confirm').mockImplementation(() => {
      return false;
    });

    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderCollapseButton = folderItem.querySelector(
      '.sidebar__folder_collapse'
    );
    folderCollapseButton?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    await new Promise((resolve) => setTimeout(resolve, 1));

    const noteItem = folderItem.querySelectorAll('.sidebar__note_item')[0];
    const deleteButton = noteItem.querySelector('.sidebar__delete_note');

    deleteButton?.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    await new Promise((resolve) => setTimeout(resolve, 1));

    expect(folderItem.querySelectorAll('.sidebar__note_item').length).toBe(2);

    expect(confirmSpy).toHaveBeenCalled();
    confirmSpy.mockRestore();
  });

  test('deletes a folder after confirmation', async () => {
    const confirmSpy = jest.spyOn(window, 'confirm').mockImplementation(() => {
      return true;
    });

    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderItemId = folderItem.id;
    const deleteButton = folderItem.querySelector(
      '.sidebar__folder_options_button'
    );

    deleteButton?.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    const deleteFolderOption = container.querySelector(
      '.sidebar__folder_dropdown_option:nth-child(2)'
    );
    deleteFolderOption?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    await new Promise((resolve) => setTimeout(resolve, 1));

    expect(container.querySelector(`folder-item-${folderItemId}`)).toBeNull();

    expect(confirmSpy).toHaveBeenCalled();
    confirmSpy.mockRestore();
  });

  test('adds a new note to a folder', async () => {
    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderCollapseButton = folderItem.querySelector(
      '.sidebar__folder_collapse'
    );
    folderCollapseButton?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    await new Promise((resolve) => setTimeout(resolve, 1));

    const noteList = folderItem.querySelector('.sidebar__note_list');
    const initialNoteCount = noteList?.children.length;

    const addNoteButton = folderItem.querySelector(
      '.sidebar__folder_options_button'
    );

    addNoteButton?.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    const addNoteOption = container.querySelector(
      '.sidebar__folder_dropdown_option:nth-child(1)'
    );
    addNoteOption?.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    await new Promise((resolve) => setTimeout(resolve, 1));

    const updatedNoteList = folderItem.querySelector('.sidebar__note_list');
    const updatedNoteCount = updatedNoteList?.children.length;

    expect(updatedNoteCount).toBe(initialNoteCount + 1);
  });

  test('deletes a folder after confirmation', async () => {
    const confirmSpy = jest.spyOn(window, 'confirm').mockImplementation(() => {
      return true;
    });

    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const folderItemId = folderItem.id;
    const deleteButton = folderItem.querySelector(
      '.sidebar__folder_options_button'
    );

    deleteButton?.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    const deleteFolderOption = container.querySelector(
      '.sidebar__folder_dropdown_option:nth-child(2)'
    );
    deleteFolderOption?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    await new Promise((resolve) => setTimeout(resolve, 1));

    expect(container.querySelector(`folder-item-${folderItemId}`)).toBeNull();

    expect(confirmSpy).toHaveBeenCalled();
    confirmSpy.mockRestore();
  });

  test('adds a new note to an empty folder', async () => {
    const emptyFolder = {
      id: '3',
      name: 'Empty Folder',
      isExpanded: false,
      notes: [],
    };
    container.innerHTML = '';
    Sidebar(container, [emptyFolder]);

    const folderItem = container.querySelector('.sidebar__folder_item');
    const folderCollapseButton = folderItem?.querySelector(
      '.sidebar__folder_collapse'
    );

    folderCollapseButton?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    await new Promise((resolve) => setTimeout(resolve, 1));

    let noteList = folderItem?.querySelector('.sidebar__note_list');
    let initialNoteCount = noteList?.children.length;
    expect(initialNoteCount).toBe(0);

    const addNoteButton = folderItem?.querySelector(
      '.sidebar__folder_options_button'
    );
    addNoteButton?.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    const addNoteOption = container.querySelector(
      '.sidebar__folder_dropdown_option:nth-child(1)'
    );
    addNoteOption?.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    await new Promise((resolve) => setTimeout(resolve, 1));

    noteList = folderItem?.querySelector('.sidebar__note_list');
    let updatedNoteCount = noteList?.children.length;
    expect(updatedNoteCount).toBe(initialNoteCount + 1);
  });

  test('does not delete folder when deletion is canceled', async () => {
    const confirmSpy = jest.spyOn(window, 'confirm').mockImplementation(() => {
      return false;
    });

    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const deleteButton = folderItem.querySelector(
      '.sidebar__folder_options_button'
    );

    deleteButton?.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    const deleteFolderOption = container.querySelector(
      '.sidebar__folder_dropdown_option:nth-child(2)'
    );
    deleteFolderOption?.dispatchEvent(
      new MouseEvent('click', { bubbles: true })
    );

    expect(container.querySelector('.sidebar__folder_item')).not.toBeNull();
    expect(confirmSpy).toHaveBeenCalled();
    confirmSpy.mockRestore();
  });

  test('hides folder options dropdown when clicking outside', async () => {
    const folderItem = container.querySelectorAll('.sidebar__folder_item')[0];
    const optionsButton = folderItem.querySelector(
      '.sidebar__folder_options_button'
    );

    optionsButton?.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    const dropdownMenu = folderItem.querySelector(
      '.sidebar__folder_dropdown_menu'
    );
    expect(dropdownMenu?.style.display).toBe('block');

    document.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    expect(dropdownMenu?.style.display).toBe('none');
  });
});
