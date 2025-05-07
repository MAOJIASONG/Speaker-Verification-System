# 交互式给说话人 alice 连录 3 句，每句 5 秒
for i in 1 2 3; do python record_wav.py alice; done

# 有一批客服 mp3，统一转 wav
python convert_to_wav.py raw_calls/


# 1. 批量抽取 + 建库
python extract_embeddings.py
python build_faiss.py

# 2. 新增用户
python add_user.py alice new_alice_01.wav

# 3. 说话人验证 / 检索
python verify.py query.wav
# Top-1 cosine = 0.84 speaker = alice
