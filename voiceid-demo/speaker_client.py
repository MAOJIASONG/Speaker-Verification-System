import asyncio, json, uuid, soundfile as sf
import websockets

PCM_CHUNK = 3200
NAMESPACE = "SpeakerVerification"

async def _wait_task_result(ws):
    while True:
        msg = json.loads(await ws.recv())
        hdr = msg.get("header", {})
        if hdr.get("name") == "TaskResult":
            return msg
        if hdr.get("status", 0) >= 40000000:
            raise RuntimeError(f'{hdr.get("status_text")}: {msg}')

async def _wait_task_started(ws):
    while True:
        msg = json.loads(await ws.recv())
        hdr = msg.get("header", {})
        if hdr.get("name") == "TaskStarted":
            break
        if hdr.get("status", 0) >= 40000000:
            raise RuntimeError(f'{hdr.get("status_text")}: {msg}')

class SpeakerClient:
    def __init__(self, token, appkey,
                 url="wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1"):
        self.ws_url = f"{url}?token={token}"
        self.appkey = appkey
        self.conn = None
        self._task_ids = {}

    async def _connect(self):
        if not self.conn:
            self.conn = await websockets.connect(self.ws_url)

    async def _start_task(self, payload):
        if not hasattr(self, "_task_ids"):
            self._task_ids = {}
        speaker_id = payload.get("speaker_id")
        if speaker_id and speaker_id not in self._task_ids:
            # Generate and save new ids for this speaker_id
            self._task_ids[speaker_id] = {
                "message_id": uuid.uuid4().hex,
                "task_id": uuid.uuid4().hex
            }
        ids = self._task_ids.get(speaker_id, {
            "message_id": uuid.uuid4().hex,
            "task_id": uuid.uuid4().hex
        })
        header = {
            "namespace": NAMESPACE,
            "name": "StartTask",
            "appkey": self.appkey,
            "message_id": ids["message_id"],
            "task_id": ids["task_id"]
        }
        await self.conn.send(json.dumps({"header": header, "payload": payload}))
        
    async def stop_task(self, speaker_id=None):
        if not self.conn:
            return
        
        ids = self._task_ids.get(speaker_id, {
            "message_id": uuid.uuid4().hex,
            "task_id": uuid.uuid4().hex
        })
        
        header = {
            "namespace": NAMESPACE,
            "name": "StopTask",
            "appkey": self.appkey,
          "message_id": ids["message_id"],
            "task_id": ids["task_id"]
        }
        await self.conn.send(json.dumps({"header": header, "payload": {}}))
        
    async def apply_digit(self, speaker_id):
        await self._connect()
        await self._start_task({"action": "ApplyDigit", "speaker_id": speaker_id})
        await _wait_task_started(self.conn)
        await self.stop_task(speaker_id)
        resp = await _wait_task_result(self.conn)
        return resp["payload"]["digit"]

    async def _stream_pcm(self, wav_path):
        data, sr = sf.read(wav_path, dtype="int16")
        assert sr == 16000, "必须 16 kHz"
        raw = data.tobytes()
        for i in range(0, len(raw), PCM_CHUNK):
            await self.conn.send(raw[i:i+PCM_CHUNK])
        await self.conn.send(b"")        # EOF

    async def enroll(self, speaker_id, digit, wav_path):
        await self._start_task({
            "action": "Enroll", "format": "pcm", "sample_rate": 16000,
            "speaker_id": speaker_id, "digit": digit
        })
        await _wait_task_started(self.conn)
        await self._stream_pcm(wav_path)
        await self.stop_task(speaker_id)
        resp = await _wait_task_result(self.conn)
        return resp["payload"]
    
    async def update(self, speaker_id, digit, wav_path):
        await self._start_task({
            "action": "Update", "format": "pcm", "sample_rate": 16000,
            "speaker_id": speaker_id, "digit": digit
        })
        await _wait_task_started(self.conn)
        await self._stream_pcm(wav_path)
        await self.stop_task(speaker_id)
        resp = await _wait_task_result(self.conn)
        return resp["payload"]

    async def verify(self, speaker_id, digit, wav_path):
        await self._start_task({
            "action": "Verify", "format": "pcm", "sample_rate": 16000,
            "speaker_id": speaker_id, "digit": digit
        })
        await _wait_task_started(self.conn)
        await self._stream_pcm(wav_path)
        await self.stop_task(speaker_id)
        resp = await _wait_task_result(self.conn)
        return resp["payload"]

    async def delete(self, speaker_id):
        await self._start_task({"action": "Delete", "speaker_id": speaker_id})
        await _wait_task_started(self.conn)
        await self.stop_task(speaker_id)
        resp = await _wait_task_result(self.conn)
        return resp["payload"]
