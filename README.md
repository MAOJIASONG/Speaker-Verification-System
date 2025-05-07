# Speaker Verification System 使用说明

本项目实现了基于 ModelScope 3D-Speaker 的说话人验证与检索系统，支持批量建库、增量添加、实时录音、格式转换等功能。

## 环境准备

1. 克隆本仓库，进入目录
2. 安装依赖（建议使用虚拟环境）：

```bash
bash setup.sh
```

如遇 `pyaudio` 安装问题，请参考相关文档安装系统依赖。

## 主要功能

### 1. 录音采集

为指定说话人录音（默认5秒）：

```bash
python record_wav.py alice
```

自定义录音时长（如10秒）：

```bash
python record_wav.py bob 10
```

录音文件保存在 `records/<spk>/` 目录下。

### 2. 批量音频格式转换

将目录下的 mp3/m4a/flac/aac 等批量转为 16kHz 单声道 wav：

```bash
python convert_to_wav.py raw_calls/
```

### 3. 批量特征提取与建库

先批量抽取音频特征，再构建 Faiss 检索库：

```bash
python extract_embeddings.py
python build_faiss.py
```

### 4. 增量添加新用户

为新用户添加录音并更新索引：

```bash
python add_user.py alice new_alice_01.wav
```

### 5. 说话人验证/检索

对查询音频进行说话人检索：

```bash
python verify.py query.wav
# 输出示例: Top-1 cosine = 0.84 speaker = alice
```

## 交互式流程示例

可参考 `run.sh` 脚本，体验完整流程。

## 依赖说明

- Python 3.8+
- torch, torchaudio, modelscope, onnxruntime-gpu, faiss-gpu, soundfile, tqdm, sounddevice, pydub, librosa, pyaudio

详见 `requirements.txt`。

## 其他

- 配置项可在 `config.py` 中调整。
- Jupyter Notebook 示例见 `run.ipynb`。

如有问题欢迎提 issue。
