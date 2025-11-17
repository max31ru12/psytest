from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.responses import FileResponse

from backend.database import save_results

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("")
async def get_test_page():
    return FileResponse("static/pages/test.html")


class SubmitTestForm(BaseModel):
    q1: int
    q2: int
    q3: int
    q4: int
    q5: int
    q6: int
    q7: int
    q8: int
    q9: int
    q10: int
    q11: int
    q12: int
    q13: int
    q14: int
    q15: int
    q16: int
    q17: int
    q18: int
    q19: int
    q20: int
    q21: int
    q22: int
    q23: int
    q24: int
    q25: int
    q26: int
    q27: int
    q28: int
    q29: int
    q30: int
    q31: int
    q32: int
    q33: int
    q34: int
    q35: int
    q36: int
    q37: int
    q38: int
    q39: int

    q17_1: Optional[str] = Field(None, alias="q17.1")
    q19_1: Optional[str] = Field(None, alias="q19.1")
    q30_1: Optional[str] = Field(None, alias="q30.1")
    q31_1: Optional[str] = Field(None, alias="q31.1")
    q32_1: Optional[str] = Field(None, alias="q32.1")
    q33_1: Optional[str] = Field(None, alias="q33.1")
    q35_1: Optional[str] = Field(None, alias="q35.1")
    q38_1: Optional[str] = Field(None, alias="q38.1")
    q39_1: Optional[str] = Field(None, alias="q39.1")

    q40: Optional[str] = None

    class Config:
        populate_by_name = True


@router.post("")
async def submit_test_form(form_data: SubmitTestForm):
    save_results(form_data)

