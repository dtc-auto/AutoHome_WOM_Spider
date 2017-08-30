# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomeWomSpiderItem(scrapy.Item):
    # 车ID
    CAR_ID = scrapy.Field()
    # 车名
    BRAND = scrapy.Field()
    MODELKEY = scrapy.Field()

    # 用户名
    USERID = scrapy.Field()

    # 购买地点
    CITY = scrapy.Field()
    # 购买时间
    BUYDATE = scrapy.Field()
    # 裸车购买价
    PRICENET = scrapy.Field()
    # 购车目的
    PURCHASE_PURPOSE = scrapy.Field()
    # 油耗
    FUELCONSUM = scrapy.Field()
    # 公里数
    MILEAGE = scrapy.Field()

    # 评分- 空间
    SPACESCORE = scrapy.Field()
    # 评分- 动力
    POWERSCORE = scrapy.Field()
    # 评分- 操控
    MANIPLTSCORE = scrapy.Field()
    # 评分- 油耗
    FUELCONSUMSCORE = scrapy.Field()
    # 评分- 舒适性
    COMFORTSCORE = scrapy.Field()
    # 评分- 外观
    APPEARANCESCORE = scrapy.Field()
    # 评分- 内饰
    INTERIORSCORE = scrapy.Field()
    # 评分- 性价比
    COSTPERFORMSCORESCORE = scrapy.Field()

    # 评论的url
    COMMENT_URL = scrapy.Field()
    # 评论标题
    HEADLINE = scrapy.Field()
    # 评论的内容
    COMMENT_CONTENT = scrapy.Field()
    # 发表时间
    PUBLISHDATE = scrapy.Field()
    # 发表方式
    PUBLISHMODE = scrapy.Field()

    # 有多少人支持这条口碑
    Supports = scrapy.Field()
    # 有多少人看过这条口碑
    Clicks = scrapy.Field()
    # 有多少人评论这条口碑
    Comments = scrapy.Field()

