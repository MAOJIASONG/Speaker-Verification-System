# aliyun_token.py
import base64
import hashlib
import hmac
import json
import os
import time
import urllib.parse

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from dotenv import load_dotenv

load_dotenv()

REGION   = os.getenv("ALIYUN_REGION_ID", "cn-shanghai")
ENDPOINT = os.getenv("ALIYUN_ENDPOINT", "nls-meta.cn-shanghai.aliyuncs.com")
AK_ID    = os.getenv("ALIYUN_AK_ID")
AK_SECRET= os.getenv("ALIYUN_AK_SECRET")
VERSION = "2019-02-28"

def get_token():
    client = AcsClient(AK_ID, AK_SECRET, REGION)

    req = CommonRequest()
    req.set_method("POST")
    req.set_domain(ENDPOINT)
    req.set_version(VERSION)
    req.set_action_name("CreateToken")

    try:
        resp = client.do_action_with_exception(req)           # 自动签名
        print(resp)
        data = json.loads(resp)
        if 'Token' in data and 'Id' in data['Token']:
            token = data["Token"]["Id"]
            expire_time = int(data["Token"]["ExpireTime"])
            print("token = " + token)
            print("expireTime = " + str(expire_time))
    except Exception as e:
        print("Error occurred while getting token:", e)
        return None, None
    
    return token, expire_time

if __name__ == "__main__":
    token, expire = get_token()
    print("Token:", token)
    print("过期时间:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expire)))
    print("剩余时间:", expire - int(time.time()), "秒")
    

def calculate_signature(access_key_secret, method, query_parameters):
    sorted_query_parameters = sorted(query_parameters.items(), key=lambda x: x[0])
    query_string = '&'.join(['{}={}'.format(k, v) for k, v in sorted_query_parameters])
    string_to_sign = 'GET&%2F&' + urllib.parse.quote(query_string, safe='')
    timestamp = int(time.time())
    date = str(timestamp)
    region = REGION

    sign_str = '{}\n{}\n{}\n{}'.format(date, region, method, string_to_sign)
    signature = base64.b64encode(hmac.new(bytes(access_key_secret + '&', encoding='utf-8'), bytes(sign_str, encoding='utf-8'), digestmod=hashlib.sha256).digest()).decode()
    return signature