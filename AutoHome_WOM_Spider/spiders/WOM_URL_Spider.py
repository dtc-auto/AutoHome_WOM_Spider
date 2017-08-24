# -*- coding: utf-8 -*-
import codecs
import re
import requests
import scrapy
from lxml import etree
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from AutoHome_WOM_Spider.modules.get_models import get_type_id
from AutoHome_WOM_Spider.items import Autohome_WOM_URL_Item
from AutoHome_WOM_Spider.modules.Restore import get_complete_text_autohome


class UrlSpiderSpider(scrapy.Spider):
    name = "WOM_URL_Spider"

    reqs = []
    car_id_list = get_type_id()
    for i in car_id_list:  # i代表从车型的遍历
        req_0 = "http://k.autohome.com.cn/%s" % str(i)
        req_1 = "http://k.autohome.com.cn/%s/stopselling" % str(i)
        reqs.append(req_0)
        reqs.append(req_1)
    start_urls = list(set(reqs))
    xpath = {
        'post': './/div[@class="title-name name-width-01"]/a',
        'next_page': './/div[@class="page"]/a[@class="page-item-next"]'
    }
    rules = (
        Rule(LinkExtractor(restrict_xpaths=xpath['post']), callback='pars', follow=True),
        Rule(LinkExtractor(restrict_xpaths=xpath['next_page']))
    )


    def parse(self, response):
        item = Autohome_WOM_URL_Item()
        text = get_complete_text_autohome(response.text)
        pattern_js = re.compile("\<b\>\<a href=\"\/\/(.+?)\"\ target")
        js_list = re.findall(pattern_js, text)
        if js_list:
            print(js_list)
            if js_list:
                for a in js_list:
                    item['CONNENT_URL'] = a
                    print(item)
                    #print('finish')
                    yield item