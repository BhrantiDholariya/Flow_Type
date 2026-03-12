# FlowType: Offline Voice-to-Text Assistant

FlowType is a lightweight, fully offline voice typing assistant for Windows. It allows you to hold a global hotkey (default: **Shift**) to record your voice, transcribe it locally using `faster-whisper`, and automatically paste the result into any active text field.

## Features
- **100% Offline**: Privacy-focused, no data leaves your machine.
- **Low Latency**: Near-instant transcription (1-2s) using Faster-Whisper with CPU int8 quantization.
- **Push-to-Talk**: Global hotkey support (hold to record).
- **Auto-Formatting**: Smart rule-based formatting (punctuation, capitalization, fillers, emojis).
- **Lightweight**: Minimal RAM usage (~300MB while active).

## Installation

### 1. Prerequisites
- Python 3.9 or higher installed on Windows.
- [FFmpeg](https://ffmpeg.org/download.html) installed and added to your system PATH (required for audio processing).

### 2. Setup Environment
Open PowerShell and run:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Model Download
The models will be downloaded automatically on the first run. By default, it uses the `tiny.en` model (~75MB). You can change this in `config.yaml`.

## Usage

1. **Activate the Venv**: `.\venv\Scripts\Activate.ps1`
2. **Run the App**: `python -m src.main`
3. **Record**: Hold the **Left Shift** (or whatever hotkey you configured) and speak.
4. **Release**: Release the key. The text will be transcribed and pasted at your cursor location.

## Configuration
Edit `config.yaml` to customize:
- `hotkey`: Change the trigger key.
- `model.size`: Use `tiny.en` for English-only (fastest) or `tiny` / `base` for multilingual support (English, Hindi, Gujarati, etc.).
- `formatting`: Toggle auto-punctuation, filler removal, etc.

## Multi-Language Support
To use Hindi or Gujarati:
1. Open `config.yaml`.
2. Change `model.size` to `"tiny"` (multilingual) or `"base"`.
3. Restart the app. Whisper will automatically detect the language being spoken.

## Performance Considerations
- **CPU Inference**: Optimized for CPU-only systems using `int8` quantization.
- **RAM**: Expect ~300-500MB usage with the `tiny` model.
- **Speed**: Transcription usually takes less than 1 second for short sentences.

## Future Android Architecture
To port this to Android, the following modules would be replaced:
- **Hotkey**: Implementation of a background service + accessibility service to listen for volume button hold.
- **Audio**: Use `AudioRecord` API or `OBOE` for low latency.
- **Inference**: Use `whisper.cpp` or TFLite version of Whisper.
- **Injection**: Use `AccessibilityService`'s `AccessibilityNodeInfo.ACTION_SET_TEXT` or IME-based approach.

## License
MIT
