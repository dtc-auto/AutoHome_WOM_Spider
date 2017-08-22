# -*- coding: UTF-8 -*-
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}



def __init__(self):
    pass

def process_request(url):  # 返回响应
    try:
        resp = requests.post(url, headers=headers)
        if resp.status_code == 200:
            return resp.text
        else:
            return process_request(url)
    except:
        # time.sleep(10)
        return process_request(url)

def get_type_id():
    start_url_list = [
        'http://www.autohome.com.cn/a00/',  # 微型车
        'http://www.autohome.com.cn/a0/',  # 小型车
        'http://www.autohome.com.cn/a/',  # 紧凑型车
        'http://www.autohome.com.cn/b/',  # 中型车
        'http://www.autohome.com.cn/c/',  # 中大型车
        'http://www.autohome.com.cn/d/',  # 大型车
        'http://www.autohome.com.cn/suv/',  # SUV
        'http://www.autohome.com.cn/mpv/',  # MPV
        'http://www.autohome.com.cn/s/',  # 跑车
        'http://www.autohome.com.cn/p/',  # 皮卡
        'http://www.autohome.com.cn/mb/',  # 微面
    ]
    models_list = []
    for url_t in start_url_list:
        model_resp = process_request(url_t)
        model_respose = etree.HTML(model_resp)
        models = model_respose.xpath('.//a/@data-value')
        models_list=models_list+models
    return models_list