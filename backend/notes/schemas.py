from typing import Optional

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from core.schemas import StrObjectId


class NoteCreate(BaseModel):
    title: str = Field(examples=["Vacations"])

    model_config = ConfigDict(extra="ignore", frozen=True)


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(default=None, examples=["My first note"])
    content: Optional[str] = Field(default=None, examples=["Once upon a time..."])
    last_updated_at: Optional[AwareDatetime] = Field(
        default=None, examples=["2022-01-01T00:00:00Z"]
    )

    model_config = ConfigDict(extra="ignore", frozen=True)


class NoteRetrieve(BaseModel):
    id: StrObjectId = Field(
        validation_alias="_id", examples=["db490d0c-8e01-4ee4-8c36-abad040a0a0c"]
    )
    title: str = Field(examples=["Vacations"])
    content: Optional[str] = Field(default=None, examples=["I will go to the beach."])
    folder_id: StrObjectId = Field(examples=["db490d0c-8e01-4ee4-8c36-abad040a0a0c"])
    last_updated_at: Optional[AwareDatetime] = Field(
        default=None, examples=["2022-01-01T00:00:00Z"]
    )
    created_at: Optional[AwareDatetime] = Field(
        examples=["2022-01-01T00:00:00Z"], default=None
    )

    model_config = ConfigDict(extra="ignore", frozen=True)
