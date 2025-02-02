from pydantic import BaseModel, ConfigDict, Field

from core.schemas import StrObjectId


class FolderRetrieve(BaseModel):
    id: StrObjectId = Field(
        validation_alias="_id", examples=["db490d0c-8e01-4ee4-8c36-abad040a0a0c"]
    )
    name: str = Field(examples=["Vacations 2024"])

    model_config = ConfigDict(extra="ignore", frozen=True)


class FolderCreate(BaseModel):
    name: str = Field(examples=["Vacations 2024"])

    model_config = ConfigDict(extra="ignore", frozen=True)


class FolderUpdate(BaseModel):
    name: str = Field(examples=["Vacations 2024"])

    model_config = ConfigDict(extra="ignore", frozen=True)
