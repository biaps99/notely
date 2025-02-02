export type Note = {
  id: string;
  title: string;
  content: string;
  folder_id: string;
  last_updated_at: string;
};

export type Folder = {
  id: string;
  name: string;
  isExpanded: boolean;
};
