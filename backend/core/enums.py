from enum import Enum


class EventType(Enum):
    pass


class NoteEventType(EventType):
    CREATED = "NOTE_CREATED"
    UPDATED = "NOTE_UPDATED"
    DELETED = "NOTE_DELETED"


class FolderEventType(EventType):
    CREATED = "FOLDER_CREATED"
    UPDATED = "FOLDER_UPDATED"
    DELETED = "FOLDER_DELETED"
