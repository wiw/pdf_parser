from attr import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Union, List
from uuid import UUID
from pydantic import EmailStr


@dataclass
class Report:
    report_name: str
    file_path: Union[str, Path]
    create_datetime: Optional[datetime] = field(factory=datetime.utcnow)


@dataclass
class Questionnaire:
    questionnaire_name: str
    file_path: Union[str, Path]
    upload_datetime: Optional[datetime] = field(factory=datetime.utcnow)
    is_processed: bool = False
    is_created_report: bool = False
    reports: Optional[List[Report]] = field(factory=list)


@dataclass
class Task:
    id: UUID
    polls_number: int
    create_datetime: Optional[datetime] = field(factory=datetime.utcnow)
    is_closed: bool = False
    processed_of_polls_number: Optional[int] = None
    questionnaires: Optional[List[Questionnaire]] = field(factory=list)


@dataclass
class Email:
    appeal: str
    full_name: str
    email_address: EmailStr
    reports: Optional[List[Report]] = field(factory=list)
