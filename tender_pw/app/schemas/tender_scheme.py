from pydantic import BaseModel

from .auth_scheme import AuthScheme


class ApplicationData(BaseModel):
    subject_address: str = "071800"
    iik: str = "KZ5696502F0017154550"
    contact_phone: str = "7014333488"


class TenderScheme(AuthScheme):
    application_data: ApplicationData
