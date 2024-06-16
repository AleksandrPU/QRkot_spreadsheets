from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class GetMixin:

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ) -> CharityProject:
        obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return obj.scalars().first()


class UpdateMixin(GetMixin):

    async def update(
            self,
            db_obj: CharityProject,
            obj_in: CharityProjectUpdate,
            session: AsyncSession
    ) -> CharityProject:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj


class DeleteMixin(GetMixin):

    async def remove(
            self,
            db_obj: CharityProject,
            session: AsyncSession
    ) -> CharityProject:
        await session.delete(db_obj)
        await session.commit()

        return db_obj
