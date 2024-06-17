from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import asc

from app.models import CharityProject

from .base import CRUDBase
from .mixins import DeleteMixin, UpdateMixin


class CRUDCharityProject(CRUDBase, UpdateMixin, DeleteMixin):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ):
        closed_projects = await session.execute(
            select([
                CharityProject.name,
                CharityProject.description,
                (
                    func.unixepoch(CharityProject.close_date, 'subsec') -
                    func.unixepoch(CharityProject.create_date, 'subsec')
                ).label('length')
            ]).where(
                CharityProject.fully_invested
            ).order_by(asc('length'))
        )
        return closed_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
