import abc
import sounddevice as sd
import numpy as np
import logging

class BaseRecorder(abc.ABC):
    @abc.abstractmethod
    def start_recording(self): pass
    
    @abc.abstractmethod
    def stop_recording(self): pass

class AudioRecorder(BaseRecorder):
    def __init__(self, sample_rate=16000, vad_threshold=0.5):
        self.sample_rate = sample_rate
        self.vad_threshold = vad_threshold
        self.recording = False
        self.audio_buffer = []
        self.stream = None

        # Load Silero VAD using the installed silero-vad package
        try:
            from silero_vad import load_silero_vad, get_speech_timestamps
            self.vad_model = load_silero_vad()
            self.get_speech_timestamps = get_speech_timestamps
            logging.info("Silero VAD loaded successfully.")
        except Exception as e:
            logging.warning(f"Silero VAD not available ({e}). VAD filtering disabled.")
            self.vad_model = None
            self.get_speech_timestamps = None

    def start_recording(self):
        self.recording = True
        self.audio_buffer = []
        logging.info("Recording started...")
        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32',
                callback=self.callback
            )
            self.stream.start()
        except Exception as e:
            logging.error(f"FAILED to open microphone: {e}")
            self.recording = False
            self.stream = None
            raise

    def stop_recording(self):
        self.recording = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        logging.info("Recording stopped.")
        if not self.audio_buffer:
            return None

        audio = np.concatenate(self.audio_buffer).flatten()
        return audio

    def callback(self, indata, frames, time, status):
        if status:
            logging.warning(f"Audio status: {status}")
        if self.recording:
            self.audio_buffer.append(indata.copy())

    def process_vad(self, audio_data):
        """Optionally filter audio using Silero VAD."""
        if audio_data is None or self.vad_model is None:
            return audio_data

        import torch
        audio_tensor = torch.from_numpy(audio_data.astype(np.float32))

        try:
            speech_timestamps = self.get_speech_timestamps(
                audio_tensor,
                self.vad_model,
                sampling_rate=self.sample_rate,
                threshold=self.vad_threshold
            )
            if not speech_timestamps:
                logging.info("VAD: No speech detected.")
                return None

            # Stitch together only the speech segments
            speech_chunks = [
                audio_data[ts['start']:ts['end']]
                for ts in speech_timestamps
            ]
            return np.concatenate(speech_chunks)
        except Exception as e:
            logging.warning(f"VAD processing failed ({e}), using raw audio.")
            return audio_data
