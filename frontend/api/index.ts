import { AxiosResponse } from 'axios';
import * as types from '../types';
import { api as fakeApi } from './fake';
import { api as axiosApi } from './axios';

type Api = {
  get: (url: string) => Promise<AxiosResponse>;
  put: (url: string, data: any) => Promise<AxiosResponse>;
  post: (url: string, data: any) => Promise<AxiosResponse>;
  delete: (url: string) => Promise<AxiosResponse>;
};

const api: Api = process.env.NODE_ENV === 'testing' ? fakeApi : axiosApi;

/**
 * Fetches a list of folders from the API.
 * @param limit - The maximum number of folders to fetch (default is 50).
 * @param offset - The number of folders to skip (default is 0).
 * @returns A promise that resolves with an array of folders.
 * @throws An error if the API request fails.
 */
const fetchFolders = async (
  limit: number = 50,
  offset: number = 0
): Promise<types.Folder[]> => {
  try {
    const response: AxiosResponse<types.Folder[]> = await api.get(
      `/folders?limit=${limit}&offset=${offset}`
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Updates a folder's details on the API.
 * @param folder - The folder data to update.
 * @param folderId - The ID of the folder to update.
 * @returns A promise that resolves with the updated folder.
 * @throws An error if the API request fails.
 */
const updateFolder = async (
  folder: Partial<types.Folder>,
  folderId: string
): Promise<types.Folder> => {
  try {
    const response: AxiosResponse<types.Folder> = await api.put(
      `/folders/${folderId}`,
      folder
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Creates a new folder on the API.
 * @param folder - The folder data to create.
 * @returns A promise that resolves with the newly created folder.
 * @throws An error if the API request fails.
 */
const createFolder = async (folder: types.Folder): Promise<types.Folder> => {
  try {
    const response: AxiosResponse<types.Folder> = await api.post(
      '/folders',
      folder
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Fetches the notes for a specific folder from the API.
 * @param folderId - The ID of the folder whose notes to fetch.
 * @returns A promise that resolves with an array of notes.
 * @throws An error if the API request fails.
 */
const fetchFolderNotes = async (folderId: string): Promise<types.Note[]> => {
  try {
    const response: AxiosResponse<types.Note[]> = await api.get(
      `/folders/${folderId}/notes`
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Updates a note's details on the API.
 * @param note - The note data to update.
 * @param noteId - The ID of the note to update.
 * @param folderId - The ID of the folder that contains the note.
 * @returns A promise that resolves with the updated note.
 * @throws An error if the API request fails.
 */
const updateNote = async (
  note: Partial<types.Note>,
  noteId: string,
  folderId: string
): Promise<types.Note> => {
  try {
    const response: AxiosResponse<types.Note> = await api.put(
      `/folders/${folderId}/notes/${noteId}`,
      note
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Deletes a note from the API.
 * @param noteId - The ID of the note to delete.
 * @param folderId - The ID of the folder that contains the note.
 * @returns A promise that resolves with the deleted note.
 * @throws An error if the API request fails.
 */
const deleteNote = async (
  noteId: string,
  folderId: string
): Promise<types.Note> => {
  try {
    const response: AxiosResponse<types.Note> = await api.delete(
      `/folders/${folderId}/notes/${noteId}`
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Creates a new note on the API.
 * @param note - The note data to create.
 * @param folderId - The ID of the folder to add the note to.
 * @returns A promise that resolves with the newly created note.
 * @throws An error if the API request fails.
 */
const createNote = async (
  note: Partial<types.Note>,
  folderId: string
): Promise<types.Note> => {
  try {
    const response: AxiosResponse<types.Note> = await api.post(
      `/folders/${folderId}/notes`,
      note
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Deletes a folder from the API.
 * @param folderId - The ID of the folder to delete.
 * @returns A promise that resolves with the deleted folder.
 * @throws An error if the API request fails.
 */
const deleteFolder = async (folderId: string): Promise<types.Folder> => {
  try {
    const response: AxiosResponse<types.Folder> = await api.delete(
      `/folders/${folderId}`
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

export {
  fetchFolders,
  updateFolder,
  createFolder,
  fetchFolderNotes,
  updateNote,
  deleteNote,
  createNote,
  deleteFolder,
};
