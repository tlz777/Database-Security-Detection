# 'ersleeer'
# 2022-08-03 18:35

import requests
from base import base64
import urllib3
# requests.packages.urllib3.disable_warnings()

'''
通用文字识别
'''

def image_ocr(path):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=fqq2vFRXkzGmFPArh5d2YBL0&client_secret=pgUz5rUqcstIUgdjbnNUHSI0sQRYD2Fd'
    response = requests.get(host)
    if response:
        print(response.json())

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    access_token = response.json()['access_token']
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()['words_result']

