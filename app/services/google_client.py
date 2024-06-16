from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import (
    COLUMN_COUNT,
    DATE_FORMAT,
    GOOGLE_SHEET_RANGE,
    ROW_COUNT,
    SHEET_ID
)


def now_date_time():
    return datetime.now().strftime(DATE_FORMAT)


async def spreadsheets_create(wrapper_service: Aiogoogle) -> str:
    service = await wrapper_service.discover('sheets', 'v4')

    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт от {now_date_time()}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': SHEET_ID,
                    'title': 'Отчёт',
                    'gridProperties': {
                        'rowCount': ROW_COUNT,
                        'columnCount': COLUMN_COUNT
                    }
                }
            }
        ]
    }

    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )

    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_service: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_service.discover('drive', 'v3')

    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_service: Aiogoogle
) -> None:
    service = await wrapper_service.discover('sheets', 'v4')

    table_values = [
        ['Отчёт от', now_date_time()],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for project in projects:
        new_row = [
            project['name'],
            str(timedelta(seconds=project['length'])),
            project['description']
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=GOOGLE_SHEET_RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
