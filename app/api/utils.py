from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud, donation_crud
from app.models import BaseProjectDonation, CharityProject, Donation
from app.services.investment import investment


async def to_investment(
        obj: BaseProjectDonation,
        session: AsyncSession
) -> BaseProjectDonation:
    """Подготовить данные для инвестирования."""

    not_invested_projects = await charity_project_crud.get_multi(
        session, not_full_invested=True)
    not_invested_donations = await donation_crud.get_multi(
        session, not_full_invested=True)

    if obj.invested_amount is None:
        setattr(obj, 'invested_amount', 0)
    if isinstance(obj, CharityProject):
        not_invested_projects.append(obj)
    elif isinstance(obj, Donation):
        not_invested_donations.append(obj)

    changed_objs = await investment(
        not_invested_projects,
        not_invested_donations
    )

    session.add_all(changed_objs)
    await session.commit()
    await session.refresh(obj)

    return obj
