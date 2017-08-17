# -*- coding: utf-8 -*-
import pymssql
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

    sql_models_id = """SELECT models FROM [source].[AutoHome_SPEC_Type] Group by models"""
    url_list = []

    car_id_list = get_list(sql_models_id)
    reqs=[]
    for i in car_id_list:  # i代表从车型的遍历
        req_0 = scrapy.Request("http://k.autohome.com.cn/%s" % (i))
        req_1 = scrapy.Request("http://k.autohome.com.cn/%s/stopselling" % (i))
        reqs.append(req_0.url)
        reqs.append(req_1.url)
        for j in range(2, 601):  # j代表评论页数，range(1,3)表示1到2页
            req_2 = scrapy.Request("http://k.autohome.com.cn/%s/index_%s.html#dataList" % (i, j))
            req_3 = scrapy.Request("http://k.autohome.com.cn/%s/stopselling/index_%s.html#dataList" % (i, j))
            reqs.append(req_2.url)
            reqs.append(req_3.url)
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
                    yield item