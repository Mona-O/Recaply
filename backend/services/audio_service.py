import sounddevice as sd
from scipy.io.wavfile import write , read
import whisper

class AudioService:
    def __init__(self):
        self.model = whisper.load_model("small")

    def transcribe_meeting(self, file):

        # FastAPI UploadFile → save temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        result = self.model.transcribe(
            tmp_path,
            language="fr"
        )

        os.remove(tmp_path)

        return result["text"]
    
    # def transcribe_meeting(file):
    #     model = whisper.load_model("small")
    #     result= model.transcribe(
    #         file,
    #         word_timestamps=True,
    #         language="fr"
    #     )
    #     print(result["text"])


