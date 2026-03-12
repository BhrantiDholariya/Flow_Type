import subprocess
import logging

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    if check_ffmpeg():
        print("FFmpeg is installed and working.")
    else:
        print("FFmpeg NOT FOUND. Please install FFmpeg and add it to your PATH.")
