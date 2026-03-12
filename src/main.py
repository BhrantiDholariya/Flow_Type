import os
import numpy as np
import time
import logging
import threading
import pyperclip
from pynput import keyboard
from src.config import config
from src.recorder import AudioRecorder
from src.transcriber import Transcriber
from src.formatter import TextFormatter
from src.utils import check_ffmpeg

# Configure Logging to both file and console
log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'flowtype.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

class FlowTypeApp:
    def __init__(self):
        if not check_ffmpeg():
            logging.warning("FFmpeg not found in PATH. This is optional — the app will still work.")
            
        self.config = config
        self.recorder = AudioRecorder(
            sample_rate=self.config.get("recording.sample_rate"),
            vad_threshold=self.config.get("recording.vad_threshold")
        )
        self.transcriber = Transcriber(
            model_size=self.config.get("model.size"),
            device=self.config.get("model.device"),
            compute_type=self.config.get("model.compute_type")
        )
        self.formatter = TextFormatter(config=self.config.get("formatting"))
        
        self.hotkey = self.config.get("hotkey", "<shift>")
        self.is_recording = False
        self.controller = keyboard.Controller()

    def on_press(self, key):
        # Handle Shift (or other non-character keys)
        try:
            k = key.name
        except AttributeError:
            k = str(key)

        if self.hotkey in k.lower() and not self.is_recording:
            self.start_process()

    def on_release(self, key):
        try:
            k = key.name
        except AttributeError:
            k = str(key)

        if self.hotkey in k.lower() and self.is_recording:
            self.stop_process()

    def start_process(self):
        self.is_recording = True
        self.recorder.start_recording()

    def stop_process(self):
        self.is_recording = False
        audio_data = self.recorder.stop_recording()
        
        if audio_data is not None:
            # Run transcription and pasting in a separate thread to avoid blocking the hotkey listener
            threading.Thread(target=self.process_audio, args=(audio_data,)).start()

    def process_audio(self, audio_data):
        if audio_data is None or len(audio_data) == 0:
            logging.info("No audio recorded.")
            return

        # Log average volume for debugging
        volume = np.abs(audio_data).mean()
        logging.info(f"Processing audio (Level: {volume:.4f})...")
        
        if volume < 0.001:
            logging.warning("Mic recording is near-silent. Check your Windows Mic settings.")

        start_time = time.time()
        
        # 1. Transcribe with enhanced settings
        beam_size = self.config.get("model.beam_size", 5)
        initial_prompt = self.config.get("model.initial_prompt", "")
        
        raw_text = self.transcriber.transcribe(
            audio_data, 
            beam_size=beam_size, 
            initial_prompt=initial_prompt
        )
        if not raw_text:
            logging.info("No speech detected.")
            return

        # 2. Format
        formatted_text = self.formatter.format(raw_text)
        
        # 3. Paste
        self.paste_text(formatted_text)
        
        duration = time.time() - start_time
        logging.info(f"Done! Processed in {duration:.2f}s. Result: {formatted_text}")

    def paste_text(self, text):
        logging.info(f"Attempting to paste: {text}")
        
        # Store current clipboard
        old_clipboard = pyperclip.paste()
        pyperclip.copy(text)
        
        # Give Windows a moment to update the clipboard
        time.sleep(0.3)
        
        # Simulate Ctrl+V
        with self.controller.pressed(keyboard.Key.ctrl):
            self.controller.press('v')
            self.controller.release('v')
            
        # Fallback: if it's a short string, we can also try typing it directly 
        # to ensure it works in apps that block Ctrl+V
        if len(text) < 50:
             logging.info("Using backup typing method for short text...")
             time.sleep(0.1)
             self.controller.type(text)
             
        time.sleep(0.2)
        pyperclip.copy(old_clipboard)

    def run(self):
        logging.info(f"FlowType is active. Hold {self.hotkey} to record.")
        # Start the listener
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            # We also need the audio inputStream to be running if it's using a callback
            # But the way recorder.py is designed now, we start/stop manually
            # Actually, recorder.py needs a sounddevice stream running or we need to use sd.rec
            # Let's fix recorder.py to use a background stream if needed or just sd.rec for duration
            
            # Since we are using push-to-talk, we can just start a stream in start_process
            # and stop it in stop_process. Let's update recorder.py slightly for better state management
            # but for now, we'll just keep the listener alive.
            listener.join()

if __name__ == "__main__":
    app = FlowTypeApp()
    app.run()
