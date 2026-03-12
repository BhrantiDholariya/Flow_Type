import abc
from faster_whisper import WhisperModel
import logging
import os

class BaseTranscriber(abc.ABC):
    @abc.abstractmethod
    def transcribe(self, audio_data, beam_size=5, initial_prompt=None): pass

class Transcriber(BaseTranscriber):
    def __init__(self, model_size="small", device="cpu", compute_type="int8"):
        logging.info(f"Loading Whisper model: {model_size}...")
        project_root = os.path.dirname(os.path.dirname(__file__))
        model_path = os.path.join(project_root, "models")
        
        # This will use the manual download folder if it exists
        self.model = WhisperModel(
            model_size, 
            device=device, 
            compute_type=compute_type,
            download_root=model_path
        )
        
    def transcribe(self, audio_data, beam_size=5, initial_prompt=None):
        """Transcribes audio data to text."""
        if audio_data is None or len(audio_data) == 0:
            return ""
            
        logging.info(f"Transcribing with beam_size={beam_size} and prompt='{initial_prompt}'")
        segments, info = self.model.transcribe(
            audio_data, 
            beam_size=beam_size,
            initial_prompt=initial_prompt
        )
        
        text = ""
        for segment in segments:
            text += segment.text
            
        return text.strip()
