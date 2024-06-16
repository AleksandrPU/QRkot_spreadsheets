from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.constants import (
    DESCRIPTION_MIN_LENGTH,
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
)


class CharityProjectCreate(BaseModel):
    name: str = Field(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH)
    description: str = Field(min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: PositiveInt

    @validator('name')
    def name_cant_be_null(cls, value):
        if value is None:
            raise ValueError('Название проекта не может быть пустым.')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(
        min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH
    )
    description: Optional[str] = Field(min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
