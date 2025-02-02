from pydantic import AwareDatetime, BaseModel, BeforeValidator, ConfigDict, Field
from pydantic.types import Annotated

# Represent an`ObjectId` as a `str`
StrObjectId = Annotated[str, BeforeValidator(str)]


class EventRetrieve(BaseModel):
    id: StrObjectId = Field(
        validation_alias="_id", examples=["db490d0c-8e01-4ee4-8c36-abad040a0a0c"]
    )
    aggregate_id: StrObjectId = Field(
        examples=["3g690d0c-23e01-54e4-8c36-abad040a0a0c"]
    )
    type: str = Field(examples=["NOTE_CREATED"])
    payload: dict = Field(examples=[{"title": "Vacations"}])
    created_at: AwareDatetime = Field(examples=["2022-01-01T00:00:00Z"])

    model_config = ConfigDict(extra="ignore", frozen=True)
