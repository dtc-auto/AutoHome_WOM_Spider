import re
import codecs
import requests
import scrapy
from lxml import etree
from AutoHome_WOM_Spider.modules.Restore import get_complete_text_autohome
from AutoHome_WOM_Spider.items import Autohome_WOM_URL_Item
from AutoHome_WOM_Spider.modules.get_models import get_type_id

class UrlSpiderSpider(scrapy.Spider):
    name = "WOM_URL_Spider"

    def get_page_number(url):
        try:
            resp = requests.get(url)
            resp.encoding = "gbk"
            text = get_complete_text_autohome(resp.text)
            text = etree.HTML(text)
            page_number = text.xpath('//span[@class="page-item-info"]/text()')
            if page_number:
                return page_number[0][1:-1]
            else:
                return 0
        except:
            f = codecs.open('failure_url.txt', 'w', 'utf-8')
            f.write(url)

    reqs = []
    car_id_list = get_type_id()
    for i in car_id_list:  # i代表从车型的遍历
        req_0 = "http://k.autohome.com.cn/%s" % str(i)
        req_1 = "http://k.autohome.com.cn/%s/stopselling" % str(i)
        reqs.append(req_0)
        reqs.append(req_1)
        # 得到页数
        sell_page_number = get_page_number(req_0)
        stop_sell_page_number = get_page_number(req_1)
        print(sell_page_number, stop_sell_page_number)
        # 遍历页数
        if sell_page_number:
            for sell_page in sell_page_number:
                req_2 = "http://k.autohome.com.cn/%s/index_%s.html#dataList" % (i, sell_page)
                reqs.append(req_2)
                print(len(reqs))

        if stop_sell_page_number:
            for stop_sell_page in stop_sell_page_number:
                req_3 = "http://k.autohome.com.cn/%s/stopselling/index_%s.html#dataList" % (i, sell_page)
                reqs.append(req_3)
                print(len(reqs))
    start_urls = reqs
    print('=======================================finish=======================================')


    def parse(self, response):
        item = Autohome_WOM_URL_Item()
        print(2)
        text = get_complete_text_autohome(response.text)
        pattern_js = re.compile("\<b\>\<a href=\"\/\/(.+?)\"\ target")
        js_list = re.findall(pattern_js, text)
        if js_list:
            print(js_list)
            if js_list:
                for a in js_list:
                    item['CONNENT_URL'] = a
                    #print('finish')
                    yield item