# -*- coding: utf-8 -*-
import json
import pymssql
import re
import pandas as pd
import scrapy
from AutoHome_WOM_Spider.Restore import *
# from AutoHome_WOM_Spider.Replace_Span import *
from AutoHome_WOM_Spider.items import AutohomeWomSpiderItem
from AutoHome_WOM_Spider.settings import *


class UrlSpiderSpider(scrapy.Spider):


    name = "WOM_Spider"

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

    sql_models_id = """SELECT models FROM [source].[AutoHome_WOM_Type] Group by models"""
    url_list = []

    car_id_list = get_list(sql_models_id)
    reqs=[]
    for i in car_id_list:  # i代表从车型的遍历
        req = scrapy.Request("http://k.autohome.com.cn/%s" % i)
        reqs.append(req.url)
    start_urls = reqs
    def parse(self, response):
        aim_url_list = []
        for j in range(1, 101): # j代表评论页数，range(1,3)表示1到2页
            aim_url = scrapy.Request("%s/index_%s.html#dataList" % (response.url, j))
            aim_url_list.append(aim_url)
            text = get_complete_text_autohome(response.text)
            pattern_js = re.compile("\<b\>\<a href=\"\/\/(.+?)\"\ target")
            js_list = re.findall(pattern_js, text)
            #print js_item
            for each in js_list:
                yield each

    def dict_flatlist(self, d, i):
        item = AutohomeWomSpiderItem()

