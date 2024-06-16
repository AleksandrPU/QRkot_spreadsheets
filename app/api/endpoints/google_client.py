import logging

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import GOOGLE_DOCS_SHEETS_URL
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.services.google_client import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value
)

router = APIRouter()

logger = logging.getLogger('uvicorn')


@router.get(
    '/',
    dependencies=[Depends(current_superuser)]
)
async def report_closed_projects(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service)
):
    """Создать отчёт в Google Docs по закрытым проектам.
    Только для суперпользователей!
    """

    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )

    spreadsheet_id = await spreadsheets_create(wrapper_service)
    await set_user_permissions(spreadsheet_id, wrapper_service)
    await spreadsheets_update_value(spreadsheet_id, projects, wrapper_service)

    report_url = f'{GOOGLE_DOCS_SHEETS_URL}{spreadsheet_id}'

    logger.warning('Отчёт создан: %s', report_url)

    return {'report': report_url}
