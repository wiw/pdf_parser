from attr import dataclass, field
from datetime import datetime
from typing import Optional, Union, List, Dict
from uuid import UUID
from pydantic import EmailStr, FilePath

raw_info = List[Dict[str, Union[str, datetime]]]


@dataclass
class Email:
    full_name: str
    email_address: EmailStr
    appeal: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None


@dataclass
class Report:
    report_name: str
    file_path: FilePath
    email: Optional[Email] = None
    create_datetime: Optional[datetime] = field(factory=datetime.utcnow)


@dataclass
class Questionnaire:
    questionnaire_name: str
    file_path: FilePath
    upload_datetime: Optional[datetime] = field(factory=datetime.utcnow)
    is_processed: bool = False
    is_created_report: bool = False
    reports: Optional[List[Report]] = field(factory=list)

    def add_reports(self, reports: raw_info):
        for report in reports:
            self.reports.append(
                Report(**report)
            )


@dataclass
class Task:
    id: UUID
    polls_number: int
    create_datetime: Optional[datetime] = field(factory=datetime.utcnow)
    is_closed: bool = False
    processed_of_polls_number: Optional[int] = None
    questionnaires: Optional[List[Questionnaire]] = field(factory=list)

    def add_questionnaires(self, q: raw_info):
        for item in q:
            self.questionnaires.append(
                Questionnaire(**item)
            )
