from pydantic import BaseSettings, EmailStr


class EmailSettings(BaseSettings):
    EMAIL_USER: str
    EMAIL_PASS: str
    EMAIL_ADDRESS: EmailStr
    EMAIL_SMTP_PORT: int
