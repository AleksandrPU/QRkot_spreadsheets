from http import HTTPStatus

from fastapi import HTTPException


class EmptyGoogleAPIOptions(HTTPException):
    def __init__(self, key: str):
        self.detail: str = f'Параметр {key} для Google API не заполнен'
        super().__init__(
            status_code=HTTPStatus.NOT_ACCEPTABLE,
            detail=self.detail
        )
