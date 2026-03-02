
from audio_service import record_meeting

def main():
    duration = 10  # seconds
    filename = "meeting.wav"

    print(f"Starting recording for {duration} seconds...")
    record_meeting(duration, filename)
    print(f"Recording saved as {filename}")

if __name__ == "__main__":
    main()