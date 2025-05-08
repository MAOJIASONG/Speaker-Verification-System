import asyncio
from aliyun_token import get_token
from speaker_client import SpeakerClient
import os
from dotenv import load_dotenv
load_dotenv()

APP_KEY    = os.getenv("ALIYUN_APP_KEY")
SPEAKER_ID = "John"
# WAV_PATH   = "speaker1_a_cn_16k.wav"   # 再次朗读相同数字
# WAV_PATH   = "speaker1_b_cn_16k.wav"   # 再次朗读相同数字
WAV_PATH   = "speaker2_a_cn_16k.wav"   # 再次朗读相同数字

async def main():
    token, _ = get_token()
    cli = SpeakerClient(token, APP_KEY)
    digit = await cli.apply_digit(SPEAKER_ID)
    print("待验证数字串：", digit)
    result = await cli.verify(SPEAKER_ID, digit, WAV_PATH)
    print("验证结果：", result)   # { "score": "96.4", "decision": 1 }

asyncio.run(main())

# b'{"ErrMsg":"","Token":{"UserId":"1029346680480915","Id":"554f4b7b75304db7b9ba353002d2697e","ExpireTime":1746817255}}'
# token = 554f4b7b75304db7b9ba353002d2697e
# expireTime = 1746817255
# 待验证数字串： 05362798
# 验证结果： {'appkey': 'H752LJC9Z9eLGqTQ', 'user_id': '1029346680480915', 'speaker_id': 'John', 'digit': '05362798', 'score': '95.257415771484375', 'decision': 1}

# b'{"ErrMsg":"","Token":{"UserId":"1029346680480915","Id":"839c5a792bd44036a7c2fa8af22826cf","ExpireTime":1746817389}}'
# token = 839c5a792bd44036a7c2fa8af22826cf
# expireTime = 1746817389
# 待验证数字串： 05369278
# 验证结果： {'appkey': 'H752LJC9Z9eLGqTQ', 'user_id': '1029346680480915', 'speaker_id': 'John', 'digit': '05369278', 'score': '62.730060577392578', 'decision': 0}

# b'{"ErrMsg":"","Token":{"UserId":"1029346680480915","Id":"80802617306841bdb5d8bf8fa5071f78","ExpireTime":1746817438}}'
# token = 80802617306841bdb5d8bf8fa5071f78
# expireTime = 1746817438
# 待验证数字串： 05368972
# 验证结果： {'appkey': 'H752LJC9Z9eLGqTQ', 'user_id': '1029346680480915', 'speaker_id': 'John', 'digit': '05368972', 'score': '38.668212890625', 'decision': 0}