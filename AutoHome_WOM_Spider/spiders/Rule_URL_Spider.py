import pymssql
import requests
from lxml import etree
import re
import pandas as pd
import scrapy
import lxml
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from AutoHome_WOM_Spider.spiders.Start_URL import URL
from AutoHome_WOM_Spider.Restore import get_complete_text_autohome
from AutoHome_WOM_Spider.items import Autohome_WOM_URL_Item
from AutoHome_WOM_Spider.settings import *

class UrlSpiderSpider(CrawlSpider):
    #re_test = requests.get('http://www.autohome.com.cn/grade/carhtml/A.html')   /div[2]/a[5]@href
    name = "Rule_URL_Spider"
    start_urls = URL.url_list
    xpath = {
        'post': './/ul[@class="rank-list-ul"]',
        'next_page': './/div[@class="page"]/a[@class="page-item-next"]'
    }
    rules = (
        Rule(LinkExtractor(allow=(r'http://k.autohome.com.cn/692/#pvareaid=103459')), callback='parse_item'

    ))

    def parse_item(self, response):
        url = response.url
        print(url)
