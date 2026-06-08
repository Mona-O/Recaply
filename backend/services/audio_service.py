from scipy.io.wavfile import write , read
import whisper
import os
import tempfile

class AudioService:

    def __init__(self):
        self.model = None

    def get_model(self):

        if self.model is None:
            self.model = whisper.load_model("small")

        return self.model

    def transcribe_meeting(self, file):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".webm"
        ) as tmp:

            tmp.write(file.file.read())
            tmp_path = tmp.name

        model = self.get_model()

        result = model.transcribe(
            tmp_path,
            language="fr"
        )

        os.remove(tmp_path)
        
        return result["text"]