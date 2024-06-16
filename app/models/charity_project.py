from sqlalchemy import Column, String, Text

from app.core.constants import NAME_MAX_LENGTH

from .base import BaseProjectDonation


class CharityProject(BaseProjectDonation):
    name = Column(String(NAME_MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
