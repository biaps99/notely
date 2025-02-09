import axios from 'axios';
import * as constants from '../constants';
import { auth } from '../auth';

export const api = () => {
  const instance = axios.create({
    baseURL: constants.API_URL,
    timeout: constants.API_TIMEOUT_IN_MILLISECONDS,
  });

  instance.interceptors.request.use(
    async (config) => {
      const token = await auth.getToken();
      if (token) config.headers['Authorization'] = `Bearer ${token}`;
      return config;
    },
    (error) => Promise.reject(error)
  );

  return instance;
};
