from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import FileResponse

from backend.database import save_results

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("")
async def get_test_page():
    return FileResponse("static/pages/test.html")


class SubmitTestForm(BaseModel):
    division: str
    total: int


@router.post("")
async def submit_test_form(data: SubmitTestForm):
    save_results(data.division, data.total)
