import numpy as np, faiss, soundfile as sf, sys
from utils import wav_to_tensor, extract_single_embedding
from config import EMB_DIM, INDEX_PATH, META_PATH, SR

spk_id, wav_path = sys.argv[1], sys.argv[2]
index = faiss.read_index(INDEX_PATH)
meta  = np.load(META_PATH, allow_pickle=True).tolist()

emb = extract_single_embedding(wav_path)        # 与 batch 同模型
index.add(emb.reshape(1,-1).astype("float32"))
meta.append((spk_id, wav_path))

faiss.write_index(index, INDEX_PATH)
np.save(META_PATH, np.array(meta, dtype="object"))
