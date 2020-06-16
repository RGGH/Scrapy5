# -*- coding: utf-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import scrapy

class YelpItem(scrapy.Item):
    co_website = scrapy.Field()
    co_tel = scrapy.Field()
    link = scrapy.Field()
    logo_url = scrapy.Field()
    lcompanyname = scrapy.Field()
    spare = scrapy.Field()
