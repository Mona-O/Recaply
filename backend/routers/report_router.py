from fastapi import APIRouter, UploadFile, File, Depends , HTTPException
from services.audio_service import AudioService
from services.llm_service import LLMService
from services.report_service import ReportService
from sqlalchemy.orm import Session
from config.database import get_db
import services.database_service as db_service
import datetime
import os
from models.update_report_request import UpdateReportRequest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import traceback
router = APIRouter()

audio_service = AudioService()
llm_service = LLMService()
report_service = ReportService(audio_service, llm_service)


@router.post("/createReport")
async def create_report(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = report_service.generate_report(file)
        print("trying to add db")
        await db_service.add_report(
            db=db,
            title=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            content=result
        )

        return {"status": "ok"}

    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erreur DB")


@router.get("/getReports")
async def get_reports(db: AsyncSession = Depends(get_db)):
    try:
        reports = await db_service.get_all_reports(db)
        return reports

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/deleteReport/{report_id}")
async def delete_report(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    success = await db_service.delete_report(db, report_id)

    if not success:
        raise HTTPException(status_code=404, detail="Report not found")

    return {"status": "deleted"}

@router.patch("/editReport/{report_id}")
async def update_report_title(
    report_id: int,
    data: UpdateReportRequest,
    db: AsyncSession = Depends(get_db)
):

    report = await db_service.update_report(db,report_id,data.title)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )


    return {"status": "updated"}