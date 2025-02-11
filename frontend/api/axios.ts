import axios from 'axios';
import * as constants from '../constants';
import { auth } from '../auth';

const api = axios.create({
  baseURL: constants.API_URL,
  timeout: constants.API_TIMEOUT_IN_MILLISECONDS,
});

api.interceptors.request.use(
  async (config) => {
    const token = await auth.getToken();
    if (token) config.headers['Authorization'] = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

export { api };
