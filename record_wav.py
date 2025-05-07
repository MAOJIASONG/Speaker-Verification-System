#!/usr/bin/env python3
"""
实时录音并保存为 data/<spk>/YYYYMMDD_HHMMSS.wav
用法:
    python record_wav.py alice        # 给 alice 录 5 秒
    python record_wav.py bob 10       # 给 bob 录 10 秒
"""
import os, sys, time, soundfile as sf
from config import SR, REC_SEC, AUDIO_DIR

try:
    import pyaudio
except ImportError:
    print("Please install pyaudio: pip install pyaudio")
    sys.exit(1)

spk = sys.argv[1]
duration = int(sys.argv[2]) if len(sys.argv) > 2 else REC_SEC
os.makedirs(f"{AUDIO_DIR}/{spk}", exist_ok=True)
ts = time.strftime("%Y%m%d_%H%M%S")
wav_path = f"{AUDIO_DIR}/{spk}/{ts}.wav"

print(f"Recording {duration}s ⇒ {wav_path} …  (Ctrl+C to abort)")

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SR, input=True, frames_per_buffer=1024)
frames = []

try:
    for _ in range(0, int(SR / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
except KeyboardInterrupt:
    print("\nRecording aborted.")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()

import numpy as np
audio = np.frombuffer(b"".join(frames), dtype=np.float32)
sf.write(wav_path, audio, SR)
print("Saved.")
