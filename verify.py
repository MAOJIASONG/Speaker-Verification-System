import faiss, numpy as np, sys
from utils import extract_single_embedding
from config import INDEX_PATH, META_PATH

query_emb = extract_single_embedding(sys.argv[1]).astype("float32")
index = faiss.read_index(INDEX_PATH)
D, I = index.search(query_emb, k:=10)    # 取前 10 相似说话人
meta = np.load(META_PATH, allow_pickle=True)
results = [(float(D[0][i]), *meta[I[0][i]]) for i in range(k)]
print("Top-1 cosine =", results[0][0], "speaker =", results[0][1])
