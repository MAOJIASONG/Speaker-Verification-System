import asyncio, sys
from aliyun_token import get_token
from speaker_client import SpeakerClient
import os
from dotenv import load_dotenv
load_dotenv()

APP_KEY    = os.getenv("ALIYUN_APP_KEY")
SPEAKER_ID = "John"
WAV_PATH   = "speaker1_a_cn_16k.wav"   # 用户朗读数字的音频

async def main():
    token, _ = get_token()
    cli = SpeakerClient(token, APP_KEY)
    digit = await cli.apply_digit(SPEAKER_ID)
    print("系统下发数字串：", digit)
    result = await cli.enroll(SPEAKER_ID, digit, WAV_PATH)
    print("注册完成：", result)

asyncio.run(main())

# b'{"ErrMsg":"","Token":{"UserId":"1029346680480915","Id":"342a7fde45af42178187e4e0a13b54b7","ExpireTime":1746817166}}'
# token = 342a7fde45af42178187e4e0a13b54b7
# expireTime = 1746817166
# 系统下发数字串： 05367982
# 注册完成： {'appkey': 'H752LJC9Z9eLGqTQ', 'user_id': '1029346680480915', 'speaker_id': 'John', 'digit': '05367982'}