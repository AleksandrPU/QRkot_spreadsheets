import logging
from http import HTTPStatus
from typing import AsyncGenerator

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
from fastapi import HTTPException

from .config import settings

logger = logging.getLogger('uvicorn')

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}

message = None
for key, value in INFO.items():
    if not value:
        message = f'Параметр {key} для Google API не заполнен'
        break
else:
    if not settings.email:
        message = 'Емайл пользователя для Google API не заполнен'

credentials = None
if message:
    logger.warning(message)
else:
    credentials = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service() -> AsyncGenerator:
    if credentials:
        async with Aiogoogle(service_account_creds=credentials) as aiogoogle:
            yield aiogoogle
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            detail=message
        )
