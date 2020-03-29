# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CoolshellItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title= scrapy.Field()
    create_time= scrapy.Field()
    author= scrapy.Field()
    content= scrapy.Field()
    comments_num= scrapy.Field()
    read_num= scrapy.Field()
    rate_num= scrapy.Field()
    rate_avg= scrapy.Field()
    url = scrapy.Field()
    tags = scrapy.Field()
