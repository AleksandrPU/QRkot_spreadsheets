from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.constants import (
    DESCRIPTION_MIN_LENGTH,
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH
)


def name_cant_be_null(value: str) -> Union[str, None]:
    if value is None:
        raise ValueError('Название проекта не может быть пустым.')
    return value


class CharityProjectCreate(BaseModel):
    name: str = Field(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH)
    description: str = Field(min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: PositiveInt

    _name_cant_be_null = validator('name', allow_reuse=True)(name_cant_be_null)


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH
    )
    description: Optional[str] = Field(min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: Optional[PositiveInt]

    _name_cant_be_null = validator('name', allow_reuse=True)(name_cant_be_null)

    class Config:
        extra = Extra.forbid
