
import sounddevice as sd
from scipy.io.wavfile import write , read


num_samples = 512


def record_meeting(duration=60, filename="meeting.wav"):
    """
    fs = 44100
    channels = 2 if platform.system() != "Darwin" else 1
    print(f"Recording for {duration} seconds...")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
        sd.wait()
        wavio.write(filename, recording, fs, sampwidth=2)
        print(f"Recording saved to {filename}")
        return filename
    except Exception as e:
        print("Error recording audio:", e)
        return None"""
    
    """
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    SAMPLE_RATE = 16000
    CHUNK = int(SAMPLE_RATE / 10)

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    data = []
    voiced_confidences = []

    frames_to_record = 50

    print("Started Recording")
    for i in range(0, frames_to_record):
        
        audio_chunk = stream.read(num_samples)
        
        
        data.append(audio_chunk)
        
        audio_int16 = np.frombuffer(audio_chunk, np.int16);

        audio_float32 = int2float(audio_int16)
        
        
        new_confidence = model(torch.from_numpy(audio_float32), 16000).item()
        voiced_confidences.append(new_confidence)
    
    print("Stopped the recording")

    plt.figure(figsize=(20,6))
    plt.plot(voiced_confidences)
    plt.show()"""


    fs = 44100  # Sample rate
    seconds = 10  

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait() 
    write('output.wav', fs, myrecording)  
    


