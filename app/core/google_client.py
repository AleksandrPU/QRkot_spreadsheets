from typing import AsyncGenerator

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
from fastapi import Depends

from .config import settings
from .exceptions import EmptyGoogleAPIOptions

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


async def check_google_api_options():
    for key, value in INFO.items():
        if not value:
            raise EmptyGoogleAPIOptions(key)
    if not settings.email:
        raise EmptyGoogleAPIOptions('email')


async def get_service_account_creds() -> ServiceAccountCreds:
    await check_google_api_options()
    return ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service(
        credentials: ServiceAccountCreds = Depends(get_service_account_creds)
) -> AsyncGenerator:
    async with Aiogoogle(service_account_creds=credentials) as aiogoogle:
        yield aiogoogle
