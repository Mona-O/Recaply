from fastapi import APIRouter, UploadFile, File
from services.audio_service import AudioService
from services.llm_service import LLMService
from services.report_service import ReportService
import os
from datetime import datetime

router = APIRouter()

audio_service = AudioService()
llm_service = LLMService()
report_service = ReportService(audio_service, llm_service)


@router.post("/createReport")
async def create_report(file: UploadFile = File(...)):

    result = report_service.generate_report(file)

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