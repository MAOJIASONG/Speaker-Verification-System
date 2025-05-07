import numpy as np, librosa
from config import SR, MODEL_ID
from modelscope.pipelines import pipeline

spk_pipe = pipeline('speaker-verification', model=MODEL_ID)

def wav_to_tensor(wav, sr):
    if wav.ndim > 1: wav = wav.mean(axis=1)
    if sr != SR: wav = librosa.resample(wav, orig_sr=sr, target_sr=SR)
    return wav.astype("float32")

def extract_single_embedding(path):
    wav, sr = librosa.load(path, sr=None)
    tensor   = wav_to_tensor(wav, sr)
    emb = spk_pipe(tensor, output_embedding=True)['embedding']
    return emb / np.linalg.norm(emb)
