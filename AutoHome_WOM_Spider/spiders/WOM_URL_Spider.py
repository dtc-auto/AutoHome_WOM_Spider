# -*- coding: utf-8 -*-
import pymssql
import requests
from lxml import etree
import re
import pandas as pd
import scrapy
from AutoHome_WOM_Spider.Restore import get_complete_text_autohome
from AutoHome_WOM_Spider.items import Autohome_WOM_URL_Item
from AutoHome_WOM_Spider.settings import *

class UrlSpiderSpider(scrapy.Spider):
    name = "WOM_URL_Spider"

    def get_list(sql):
        server = DATABASE_SERVER_NAME
        user = DATABASE_USER_NAME
        password = DATABASE_USER_PASSWORD
        database = DATABASE_NAME
        host = DATABASE_HOST
        conn = pymssql.connect(user=user,
                               password=password,
                               host=host,
                               database=database)
        list_df = pd.read_sql_query(sql, conn)
        sql_url = list_df.values.tolist()
        sql_list = []
        for id in sql_url:
            sql_list.append(id[0])
        return sql_list

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
            return 0
    #all_page_number = get_page_number('http://k.autohome.com.cn/1004')

    sql_models_id = """SELECT models FROM [source].[AutoHome_SPEC_Type] Group by models"""

    car_id_list = get_list(sql_models_id)
    reqs = []
    for i in car_id_list:  # i代表从车型的遍历
        req_0 = "http://k.autohome.com.cn/%s" % (i)
        req_1 = "http://k.autohome.com.cn/%s/stopselling" % (i)
        reqs.append(req_0)
        reqs.append(req_1)
        # 得到页数
        sell_page_number = get_page_number(req_0)
        stop_sell_page_number = get_page_number(req_1)
        # 遍历页数
        if sell_page_number:
            for sell_page in sell_page_number:
                req_2 = "http://k.autohome.com.cn/%s/index_%s.html#dataList" % (i, sell_page)
                reqs.append(req_2)

        if stop_sell_page_number:
            for stop_sell_page in stop_sell_page_number:
                req_3 = "http://k.autohome.com.cn/%s/stopselling/index_%s.html#dataList" % (i, sell_page)
                reqs.append(req_3)
                print(len(reqs))
    start_urls = reqs


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
                    #print('finish')
                    yield item