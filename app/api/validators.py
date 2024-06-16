from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка уникальности имени проекта."""

    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка существования проекта."""

    project = await charity_project_crud.get(project_id, session)

    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=f'Проект с идентификатором {project_id} не существует.'
        )

    return project


async def check_project_open(
        project: CharityProject,
) -> None:
    """Проверка, что проект открыт для инвестирования."""

    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_project_empty(
        project: CharityProject,
) -> None:
    """Проверка отсутствия инвестиций в проекте."""

    if project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_project_full_amount(
        project: CharityProject,
        full_amount: int,
) -> None:
    """Проверка, сумма проекта не меньше уже проинвестированной суммы."""

    if project.invested_amount > full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить значение full_amount '
                   'меньше уже вложенной суммы.'
        )
