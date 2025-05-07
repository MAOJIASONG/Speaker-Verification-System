#!/usr/bin/env python3
"""
批量转码到 16 kHz/mono WAV。
把 mp3/m4a/flac/aac… 文件转到与原文件同目录，后缀改 .wav
默认会跳过已存在同名 wav，支持递归子目录。
用法:
    python convert_to_wav.py <dir_or_file> [more_dir_or_file ...]
"""
import sys, os, glob
from pydub import AudioSegment
from tqdm import tqdm
from config import SR

def convert(path):
    if path.lower().endswith(".wav"):
        return
    dst = os.path.splitext(path)[0] + ".wav"
    if os.path.exists(dst):
        return
    audio = AudioSegment.from_file(path)
    audio = audio.set_frame_rate(SR).set_channels(1)
    audio.export(dst, format="wav")

targets = []
for p in sys.argv[1:]:
    if os.path.isdir(p):
        targets += glob.glob(f"{p}/**/*.*", recursive=True)
    else:
        targets.append(p)

for f in tqdm(targets):
    try:
        convert(f)
    except Exception as e:
        print("skip", f, e)
