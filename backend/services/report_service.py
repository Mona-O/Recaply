print("Report service SERVICE LOADED")
class ReportService:
    def __init__(self, audio_service, llm_service):
        self.audio_service = audio_service
        self.llm_service = llm_service
        
    def generate_report(self,file):
        transcription = self.audio_service.transcribe_meeting(file)
        return self.llm_service.generate_report_LLM(transcription)
