import os, glob, time, numpy as np
import soundfile as sf
import onnxruntime as ort
from tqdm import tqdm
from utils import wav_to_tensor
from config import MODEL_ID, DATA_ROOT, BATCH, SR, EMB_DIM

# ① 下载并缓存 3D-Speaker ONNX 权重
from modelscope.pipelines import pipeline
spk_pipe = pipeline('speaker-verification', model=MODEL_ID, model_revision='onnx')

sess = ort.InferenceSession(spk_pipe.model.onnx_path, providers=['CUDAExecutionProvider'])

def batch_infer(wavs):
    ort_inputs = {'input': np.stack(wavs, axis=0)}
    emb = sess.run(None, ort_inputs)[0]          # (N, EMB_DIM)
    return emb / np.linalg.norm(emb, axis=1, keepdims=True)

def iter_wavs():
    for spk in sorted(os.listdir(DATA_ROOT)):
        for path in glob.glob(f"{DATA_ROOT}/{spk}/*.wav"):
            wav, _ = sf.read(path)
            yield spk, path, wav_to_tensor(wav, SR)

def main():
    buf_spk, buf_path, buf_wav = [], [], []
    embs, metas = [], []
    for spk, path, tensor in tqdm(iter_wavs(), total=sum(1 for _ in iter_wavs())):
        buf_spk.append(spk); buf_path.append(path); buf_wav.append(tensor)
        if len(buf_wav) == BATCH:
            embs.append(batch_infer(buf_wav))
            metas.extend(zip(buf_spk, buf_path))
            buf_spk, buf_path, buf_wav = [], [], []
    # 余数
    if buf_wav:
        embs.append(batch_infer(buf_wav))
        metas.extend(zip(buf_spk, buf_path))
    np.save("embeddings.npy", np.vstack(embs))
    np.save("metas.npy", np.array(metas, dtype="object"))
if __name__ == "__main__":
    main()
