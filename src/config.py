import yaml
import os
from pathlib import Path

DEFAULT_CONFIG = {
    "model": {
        "size": "tiny.en",
        "device": "cpu",
        "compute_type": "int8"
    },
    "recording": {
        "sample_rate": 16000,
        "channels": 1,
        "chunk_size": 1024,
        "vad_threshold": 0.5
    },
    "hotkey": "<shift>",  # Default hotkey: Shift (hold to record)
    "formatting": {
        "auto_punctuate": True,
        "auto_capitalize": True,
        "remove_fillers": True,
        "convert_emojis": True
    },
    "ui": {
        "sounds_enabled": True
    }
}

class Config:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.settings = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    self._update_recursive(self.settings, user_config)

    def _update_recursive(self, base, update):
        for k, v in update.items():
            if isinstance(v, dict) and k in base:
                self._update_recursive(base[k], v)
            else:
                base[k] = v

    def get(self, key, default=None):
        keys = key.split(".")
        val = self.settings
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val

config = Config()
