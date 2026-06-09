from fastapi import APIRouter, UploadFile, File, Depends , HTTPException
from services.audio_service import AudioService
from services.llm_service import LLMService
from services.report_service import ReportService
from sqlalchemy.orm import Session
from config.database import get_db
import services.database_service as db_service
import datetime
import os
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

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
        result = await report_service.generate_report(file)

        await db_service.add_report(
            db=db,
            title=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            content=result
        )

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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