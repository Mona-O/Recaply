from fastapi import APIRouter, UploadFile, File, Depends
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
async def create_report(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    result="result"
    #await result = report_service.generate_report(file)
    #db_service = ReportDBService(db)
    report = await db_service.add_report(db=db,
        title=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        content=result
    )

    # dossier de sortie
    output_dir = "generated_reports"
    os.makedirs(output_dir, exist_ok=True)

    # nom unique
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join(output_dir, filename)

    # sauvegarde du markdown
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(result)

    return {
        "report": result,
        "file_saved_at": filepath
    }
    
#get report
# [
#   {
#     "id": 1,
#     "filename": "report_20260608.md",
#     "content": "# Compte-rendu...",
#     "created_at": "2026-06-08T11:00:00"
#   }
# ]