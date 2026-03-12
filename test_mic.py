import sounddevice as sd
try:
    print("Listing available audio devices:")
    print(sd.query_devices())
    print("\nDefault Input Device:", sd.default.device[0])
    
    # Try a 1-second recording test
    duration = 1  # seconds
    fs = 16000
    print(f"\nAttempting a {duration}-second test recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Recording test SUCCESSFUL!")
except Exception as e:
    print(f"\nERROR accessing microphone: {e}")
