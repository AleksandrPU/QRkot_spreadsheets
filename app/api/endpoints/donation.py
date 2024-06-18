from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate,
    DonationDBSuperUser,
    DonationDBUser
)
from app.services.investment import investment

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
    not_invested_projects = await charity_project_crud.get_multi(
        session, not_full_invested=True)
    not_invested_donations = await donation_crud.get_multi(
        session, not_full_invested=True)
    new_donation.invested_amount = 0
    not_invested_donations.append(new_donation)
    changed_objs = await investment(
        not_invested_projects,
        not_invested_donations
    )

    session.add_all(changed_objs)
    await session.commit()
    await session.refresh(new_donation)

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
