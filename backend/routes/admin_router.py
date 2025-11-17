from fastapi import APIRouter
from starlette.responses import FileResponse, StreamingResponse

from backend.database import get_csv_results, get_results, get_xlsx_results

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("")
async def get_admin_page():
    return FileResponse("static/pages/admin.html")


@router.get("/test/results")
async def get_test_results():
    return get_results()


@router.get("/test/results/count")
async def get_test_results_count():
    return len(get_results())


@router.get("/test/results/csv")
async def get_test_results_csv():
    data = get_csv_results()
    return StreamingResponse(
        data,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": 'attachment; filename="results.csv"'
        }
    )


@router.get("/test/results/xlsx")
async def get_test_results_xlsx():
    data = get_xlsx_results()
    return StreamingResponse(
        data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="results.xlsx"'
        }
    )


