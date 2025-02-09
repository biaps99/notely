const OkMessage = {
  data: [],
  status: 200,
  statusText: 'OK',
};

export const api = {
  get(url: string): Promise<any> {
    return new Promise((resolve) => {
      resolve(OkMessage);
    });
  },

  put(url: string, data: any): Promise<any> {
    return new Promise((resolve) => {
      resolve(OkMessage);
    });
  },

  post(url: string, data: any): Promise<any> {
    return new Promise((resolve) => {
      resolve(OkMessage);
    });
  },

  delete(url: string): Promise<any> {
    return new Promise((resolve) => {
      resolve(OkMessage);
    });
  },
};
