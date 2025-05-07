import faiss, numpy as np
from config import EMB_DIM, INDEX_PATH, META_PATH

embs  = np.load("embeddings.npy").astype("float32")
index = faiss.index_factory(EMB_DIM, "IVF4096_PQ64", faiss.METRIC_INNER_PRODUCT)
index.train(embs)                 # 仅需一次
index.add(embs)                   # 建库
faiss.write_index(index, INDEX_PATH)
np.save(META_PATH, np.load("metas.npy", allow_pickle=True))
