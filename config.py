# 模型与路径
MODEL_ID = "iic/speech_eres2net_large_sv_zh-cn_3dspeaker_16k"  # 官网 ModelScope 名称
EMB_DIM  = 192                                  # ECAPA 预设向量维度 :contentReference[oaicite:5]{index=5}
SR       = 16000
BATCH    = 64

# 数据根目录：每个说话人一个子文件夹
DATA_ROOT = "embeddings"
AUDIO_DIR = "records"          # 录音保存目录
REC_SEC   = 5

# 索引持久化
INDEX_PATH = "faiss_index.ivfpq"
META_PATH  = "spk_meta.npy"     # 保存 [spkid, wav_path]→row_id 的映射
