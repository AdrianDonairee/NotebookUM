from pydantic import BaseModel, Field


class FunctionalityBase(BaseModel):
    name: str = Field(min_length=1)
    description: str = ""


class FunctionalityCreate(FunctionalityBase):
    pass


class FunctionalityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = None


class Functionality(FunctionalityBase):
    id: int
