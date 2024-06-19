from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import to_investment
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate,
    DonationDBSuperUser,
    DonationDBUser
)

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDBUser,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Добавить пожертвование.
    Только для зарегистрированных пользователей!
    """

    new_donation = await donation_crud.create(donation, session, user)

    new_donation = await to_investment(new_donation, session)

    return jsonable_encoder(new_donation)


@router.get(
    '/',
    response_model=list[DonationDBSuperUser],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Вывести все пожертвования.
    Только для суперпользователей!
    """

    donations = await donation_crud.get_multi(session)
    return jsonable_encoder(donations)


@router.get(
    '/my',
    response_model=list[DonationDBUser],
    response_model_exclude_none=True,
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Вывести пожертвования текущего пользователя.
    Только для зарегистрированных пользователей.
    """

    donations = await donation_crud.get_by_user(session, user)
    return jsonable_encoder(donations)
