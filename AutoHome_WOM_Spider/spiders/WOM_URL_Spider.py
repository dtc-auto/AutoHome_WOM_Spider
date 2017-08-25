# -*- coding: utf-8 -*-
import codecs
import re
import requests
import scrapy
from lxml import etree
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from AutoHome_WOM_Spider.modules.get_models import get_type_id
from AutoHome_WOM_Spider.items import AutohomeWomSpiderItem
from AutoHome_WOM_Spider.modules.Restore import get_complete_text_autohome


class UrlSpiderSpider(CrawlSpider):
    name = "WOM_URL_Spider"

    reqs = []
    car_id_list = get_type_id()
    for i in car_id_list:  # i代表从车型的遍历
        req_0 = "http://k.autohome.com.cn/%s" % str(i)
        req_1 = "http://k.autohome.com.cn/%s/stopselling" % str(i)
        reqs.append(req_0)
        reqs.append(req_1)
    start_urls = list(set(reqs))
    # start_urls = ["http://k.autohome.com.cn/spec/16903/#pvareaid=102175"]
    xpath = {
        'post': './/div[@class="title-name name-width-01"]/a',
        'next_page': './/a[@class="page-item-next"]'
    }
    rules = (
        Rule(LinkExtractor(restrict_xpaths=xpath['post']), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=xpath['next_page']))
    )

    def parse_item(self, response):
        item = AutohomeWomSpiderItem()
        text = get_complete_text_autohome(response.text)
        item['COMMENT_URL'] = response.url


        yield item