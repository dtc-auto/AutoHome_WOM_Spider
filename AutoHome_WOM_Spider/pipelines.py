# -*- coding: utf-8 -*-
import pymssql
from datetime import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutohomeWomSpiderPipeline(object):
    def __init__(self, server, user, password, database, host, into_sql, star_spider_name):
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.into_sql = into_sql
        self.star_spider_name = star_spider_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            server=crawler.settings.get('DATABASE_SERVER_NAME'),
            user=crawler.settings.get('DATABASE_USER_NAME'),
            password=crawler.settings.get('DATABASE_USER_PASSWORD'),
            database=crawler.settings.get('DATABASE_NAME'),
            host=crawler.settings.get('DATABASE_HOST'),
            into_sql=crawler.settings.get('INTO_SQL'),
            star_spider_name=crawler.settings.get('STAR_SPIDER_NAME')
        )

    def open_spider(self, spider):
        self.conn = pymssql.connect(user=self.user, password=self.password, host=self.host, database=self.database, charset='utf8',)

    def process_item(self, item, spider):
        if self.into_sql == 1:
            if self.star_spider_name == 'WOM_URL_Spider':
                self.url_spider_into(item, spider)

        return item
        # 便于理解,根据spider_name，分2次写入sql

    def url_spider_into(self, item, spider):
        cur = self.conn.cursor()
        self.conn.autocommit(True)
        CAR_ID = item['CAR_ID']
        BRAND = item['BRAND']
        MODELKEY = item['MODELKEY']
        USERID = item['USERID']
        CITY = item['CITY']
        BUYDATE = item['BUYDATE']
        PRICENET = item['PRICENET']
        PURCHASE_PURPOSE = item['PURCHASE_PURPOSE']
        FUELCONSUM = item['FUELCONSUM']
        MILEAGE = item['MILEAGE']

        SPACESCORE = item['SPACESCORE']
        POWERSCORE = item['POWERSCORE']
        MANIPLTSCORE = item['MANIPLTSCORE']
        FUELCONSUMSCORE = item['FUELCONSUMSCORE']
        COMFORTSCORE = item['COMFORTSCORE']
        APPEARANCESCORE = item['APPEARANCESCORE']
        INTERIORSCORE = item['INTERIORSCORE']
        COSTPERFORMSCORESCORE = item['COSTPERFORMSCORESCORE']
        COMMENT_URL = item['COMMENT_URL']
        HEADLINE = item['HEADLINE']
        COMMENT_CONTENT = item['COMMENT_CONTENT']


        PUBLISHDATE = item['PUBLISHDATE']
        PUBLISHMODE = item['PUBLISHMODE']
        Supports = item['Supports']
        Clicks = item['Clicks']
        Comments = item['Comments']

        # 设置时间
        last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""INSERT INTO BDCI_AUTOHOME_new.stg.AutoHome_WOM_all
                              (CAR_ID,BRAND,MODELKEY,USERID,CITY,BUYDATE,PRICENET,PURCHASE_PURPOSE,FUELCONSUM,MILEAGE,SPACESCORE,
                              POWERSCORE,MANIPLTSCORE,FUELCONSUMSCORE,COMFORTSCORE,APPEARANCESCORE,INTERIORSCORE,COSTPERFORMSCORESCORE,
                              COMMENT_URL,HEADLINE,COMMENT_CONTENT,PUBLISHDATE,PUBLISHMODE,Supports,Clicks,Comments,
                              last_update_time,create_time
                              )
                          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                                  %s,%s,%s,%s,%s,%s,%s,%s)""",
                      (CAR_ID, BRAND, MODELKEY, USERID, CITY, BUYDATE, PRICENET, PURCHASE_PURPOSE, FUELCONSUM, MILEAGE,
                        SPACESCORE,POWERSCORE, MANIPLTSCORE, FUELCONSUMSCORE, COMFORTSCORE, APPEARANCESCORE, INTERIORSCORE, COSTPERFORMSCORESCORE, COMMENT_URL, HEADLINE,
                        COMMENT_CONTENT,PUBLISHDATE, PUBLISHMODE, Supports, Clicks, Comments, last_update_time, create_time
                        ))

        self.conn.autocommit(False)
        self.conn.commit()