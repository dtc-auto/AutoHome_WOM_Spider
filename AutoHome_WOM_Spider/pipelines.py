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
        self.conn = pymssql.connect(user=self.user, password=self.password, host=self.host, database=self.database)

    def process_item(self, item, spider):
        if self.into_sql == 1:
            if self.star_spider_name == 'WOM_URL_Spider':
                self.url_spider_into(item, spider)

        return item
        # 便于理解,根据spider_name，分2次写入sql

    def url_spider_into(self, item, spider):
        cur = self.conn.cursor()
        self.conn.autocommit(True)
        connent_url = item['CONNENT_URL'],

        create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""INSERT INTO BDCI_AUTOHOME_new.stg.AutoHome_WOM_Type
                              (connent_url, create_time, last_update_time)
                          VALUES (%s,%s,%s)"""
                    , (connent_url, create_time, last_update_time))

        self.conn.autocommit(False)
        self.conn.commit()