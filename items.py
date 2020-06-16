# -*- coding: utf-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import scrapy

class YelpItem(scrapy.Item):

    link = scrapy.Field()
    logo_url = scrapy.Field()
    lcompanyname = scrapy.Field()
    spare = scrapy.Field()
