import sounddevice as sd
from scipy.io.wavfile import write , read
import whisper

num_samples = 512

""" 
    record meeting might be in frontend when adding one, keeping this for dev  
"""
def record_meeting(duration=60, filename="meeting.wav"):
    fs = 44100  # Sample rate
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait() 
    write(filename, fs, myrecording)  
    return filename
    
"""
Model to test, maybe needs to be upgraded?
"""
def transcribe_meeting(file):
    model = whisper.load_model("small")
    result= model.transcribe(
        file,
        word_timestamps=True,
        language="fr"
    )
    print(result["text"])


