from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_empty,
    check_project_exists,
    check_project_full_amount,
    check_project_open,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import close_project_donation, investment

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """Вывести все текущие проекты."""

    projects = await charity_project_crud.get_multi(session)
    return jsonable_encoder(projects)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Добавить проект.
    Только для суперпользователей!
    """

    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    new_project = await investment(new_project, session)
    return jsonable_encoder(new_project)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удалить неинвестированный проект.
    Только для суперпользователей!
    """

    project = await check_project_exists(project_id, session)
    await check_project_open(project)
    await check_project_empty(project)

    project = await charity_project_crud.remove(project, session)
    return jsonable_encoder(project)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
        project_id: int,
        project_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Изменить проект.
    Только для суперпользователей!
    """

    project = await check_project_exists(project_id, session)
    await check_project_open(project)

    if project_in.name is not None:
        await check_name_duplicate(project_in.name, session)

    if project_in.full_amount is not None:
        await check_project_full_amount(project, project_in.full_amount)

    project = await charity_project_crud.update(project, project_in, session)
    project = await close_project_donation(project)
    project = await investment(project, session)

    return jsonable_encoder(project)
