from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import BaseProjectDonation


class Donation(BaseProjectDonation):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
