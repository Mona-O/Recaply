from fastapi import APIRouter, UploadFile, File
from services.audio_service import AudioService
from services.llm_service import LLMService
from services.report_service import ReportService

router = APIRouter()

audio_service = AudioService()
llm_service = LLMService()
report_service = ReportService(audio_service, llm_service)


@router.post("/createReport")
async def create_report(file: UploadFile = File(...)):

    result = report_service.generate_report(file)

    return {
        "report": result
    }