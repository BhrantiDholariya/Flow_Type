# FlowType — Offline Voice-to-Text for Windows

FlowType is a lightweight, fully offline voice typing assistant for Windows. Hold a hotkey, speak, and your words are instantly transcribed and pasted into any text field — no internet, no cloud, no data leaving your machine.

---

## What It Does

- **Push-to-Talk**: Hold a configurable hotkey (e.g. `Ctrl+Alt`) and speak. Release to transcribe.
- **Offline Transcription**: Uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) locally on your CPU — no API calls, no internet required.
- **Auto-Formatting**: Automatically handles punctuation, capitalization, and filler word removal.
- **Clipboard-Safe Pasting**: Intelligently types or pastes the result at your cursor without overwriting your clipboard permanently.
- **Multi-Language**: Supports English, Hindi, Gujarati, and more — depending on the Whisper model selected.

---

## Tech Stack

| Component | Library |
|---|---|
| Speech Recognition | `faster-whisper` (CTranslate2) |
| Audio Recording | `sounddevice` |
| Hotkey Listening | `pynput` |
| Clipboard | `pyperclip` |
| Config | `PyYAML` |

