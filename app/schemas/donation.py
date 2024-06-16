from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):
    comment: Optional[str]
    full_amount: PositiveInt


class DonationDBUser(DonationCreate):
    id: int
    create_date: datetime


class DonationDBSuperUser(DonationDBUser):
    user_id: int
    full_amount: int
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: Optional[datetime] = None
