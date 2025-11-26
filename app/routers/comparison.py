from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.services.comparison import ComparisonService
from app.schemas.comparison import ComparisonResponse

router = APIRouter(prefix="/comparison", tags=["comparison"])

# Get the templates directory
templates_dir = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

comparison_service = ComparisonService()


@router.get("/", response_class=HTMLResponse)
async def comparison_index(request: Request):
    """Serve the upload page"""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/results", response_class=HTMLResponse)
async def comparison_results(request: Request):
    """Serve the results page (will be populated via JavaScript after upload)"""
    return templates.TemplateResponse("results.html", {"request": request})


@router.post("/api/compare", response_class=JSONResponse)
async def api_compare(
    excel_file: UploadFile = File(..., description="Excel file with 正解データ and Robota結果 tabs"),
):
    """
    API endpoint for comparing tabs within an Excel file. Returns JSON response.
    """
    try:
        # Read file content
        file_content = await excel_file.read()

        # Perform comparison
        result = comparison_service.compare_files(file_content)

        return ComparisonResponse(success=True, result=result).model_dump()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

