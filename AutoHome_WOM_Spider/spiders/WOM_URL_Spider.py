# -*- coding: utf-8 -*-
import codecs
import re
import requests
import scrapy
from lxml import etree
from AutoHome_WOM_Spider.settings import *
from AutoHome_WOM_Spider.modules.SAVE_WEB_SOURCE import Save_Source
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

        # 存储网页源代码
        url = response.url
        file_name = re.findall(r"spec\/(.+?)\/view", url)[0]
        if SAVE_SOURCE_DATA == 1:
            Save_Source(str(response.body), file_name)


        item = AutohomeWomSpiderItem()
        text_original = get_complete_text_autohome(response.text)
        text = etree.HTML(text_original)
        item['USERID'] = str(text.xpath('.//a[@id="ahref_UserId"]/text()')[0])
        car_name_list = text.xpath('.//dl[@class="choose-dl"]/dd/a/text()')
        item['CAR_ID'] = str(text.xpath('.//dl[@class="choose-dl"]/dd/a/@href')[1].replace("/", "").replace("spec", ""))
        item['CITY'] = str(text.xpath('.//dl[@class="choose-dl"][2]/dd/text()')[0].replace("\n", "").replace("\r", "").replace(" ", "").replace("\xa0", ""))
        item['BRAND'] = str(car_name_list[0])
        item['MODELKEY'] = str(car_name_list[1])
        item['BUYDATE'] = str(text.xpath('.//dd[@class="font-arial bg-blue"]/text()')[0])
        item['PRICENET'] = str(text.xpath('.//dd[@class="font-arial bg-blue"]/text()')[1].replace("\n", "").replace("\r", "").replace(" ", ""))
        FUELCONSUM_MILEAGE_list = text.xpath('.//dd[@class="font-arial bg-blue"]/p/text()')
        if FUELCONSUM_MILEAGE_list:
            item['FUELCONSUM'] = str(FUELCONSUM_MILEAGE_list[0])
            item['MILEAGE'] = str(FUELCONSUM_MILEAGE_list[1])
        score_list = text.xpath('.//span[@class="font-arial c333"]/text()')
        item['SPACESCORE'] = str(score_list[0])
        item['POWERSCORE'] = str(score_list[1])
        item['MANIPLTSCORE'] = str(score_list[2])
        item['FUELCONSUMSCORE'] = str(score_list[3])
        item['COMFORTSCORE'] = str(score_list[4])
        item['APPEARANCESCORE'] = str(score_list[5])
        item['INTERIORSCORE'] = str(score_list[6])
        item['COSTPERFORMSCORESCORE'] = str(score_list[7])
        item['PURCHASE_PURPOSE'] = str(','.join(text.xpath('.//p[@class="obje"]/text()')))
        item['HEADLINE'] = str(text.xpath('.//div[@class="kou-tit"]/h3/text()')[0])  # 标题
        item['PUBLISHDATE'] = text.xpath('.//div[@class="mouth-item"]/div/div/b/text()')
        # 定位最早发表评论时间
        if type(item['PUBLISHDATE']) == list:
            len_list = len(item['PUBLISHDATE'])
            item['PUBLISHDATE'] = str(item['PUBLISHDATE'][len_list-1])
        item['PUBLISHMODE'] = str("".join(text.xpath('.//div[@class="title-name name-width-01"]/span/text()')))
        item['COMMENT_URL'] = str(response.url)
        item['Clicks'] = str(text.xpath('.//span[@class="fn-left font-arial mr-20"]/span/text()')[0])
        item['Supports'] = str(text.xpath('.//label[@class="supportNumber"]/text()')[0])
        item['Comments'] = str(text.xpath('.//span[@class="font-arial CommentNumber"]/text()')[0])

        #  设置断点
        # pattern = re.compile("class=\"kou-tit\"(.*)", re.S)
        # text_original_cut = re.findall(pattern, response.text)[0]
        # text_original_cut = get_complete_text_autohome(text_original_cut)
        # item['COMMENT_CONTENT'] = re.search("<!--@HS_BASE64@-->.*<!--@HS_ZY@-->", text_original_cut).group().replace("<!--@HS_BASE64@-->","").replace("<!--@HS_ZY@-->", "").replace("<br/>","")


        #response.encoding = "gbk"
        pattern = re.compile("class=\"kou-tit\"(.*)", re.S)
        text = re.findall(pattern, response.text)[0]
        text = get_complete_text_autohome(text)
        item['COMMENT_CONTENT'] = str(re.search("<!--@HS_BASE64@-->.*<!--@HS_ZY@-->", text).group().replace(
            "<!--@HS_BASE64@-->", "").replace("<!--@HS_ZY@-->", "").replace("<br/>", ""))

        yield item