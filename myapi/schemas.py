from ninja import Schema
from datetime import datetime
from pydantic import Field

class DocumentIn(Schema):
    doc_name: str = Field(min_length=3, max_length=50)

class DocumentOut(Schema):
    id: int
    doc_name: str
    document: str
    file_type: str
    status: str
    uploaded_at: datetime