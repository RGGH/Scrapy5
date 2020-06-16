#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

''' Spider for Yelp '''

import json
import scrapy
from scrapy.loader import ItemLoader
from items import YelpItem
import requests
from pprint import pprint
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess



class YelpSpider(scrapy.Spider):

    name = 'yelp-spider'
    custom_settings = {'FEED_FORMAT':'csv','FEED_URI':'YELP.csv'}
    start_urls = ['https://www.yelp.com/search?find_desc=Plumbers&find_loc=London&ns=1']
    headers = {
        'user-agent' :
        'User-Agent: Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
        }

    def start_requests(self):
            # Starting url
            url = 'https://www.yelp.com/search?find_desc=Plumbers&find_loc=London&ns=1'
            # crawl next page URL
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self,response):
        # Iterate through 20 adverts per page
        all_ads =  response.xpath('.//*[@class="lemon--div__373c0__1mboc container__373c0__3HMKB hoverable__373c0__VqkG7 margin-t3__373c0__1l90z margin-b3__373c0__q1DuY padding-t3__373c0__1gw9E padding-r3__373c0__57InZ padding-b3__373c0__342DA padding-l3__373c0__1scQ0 border--top__373c0__3gXLy border--right__373c0__1n3Iv border--bottom__373c0__3qNtD border--left__373c0__d1B7K border-color--default__373c0__3-ifU"]')
        for ads in all_ads:

            l = ItemLoader(item=YelpItem(), selector=ads, response=response)

            # Get Link to detail page (20 per page)
            l.add_xpath('link', ".//a[@class='lemon--a__373c0__IEZFH link__373c0__1G70M photo-box-link__373c0__1YC9Y link-color--blue-dark__373c0__85-Nu link-size--default__373c0__7tls6']/@href")
            # Get link to image logo (23 at moment)
            l.add_xpath('logo_url', ".//img[@class='lemon--img__373c0__3GQUb photo-box-img__373c0__35y5v']/@src")

            # Get Compnay Name
            l.add_xpath('lcompanyname', ".//*[@class='lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE']/@name")
            yield l.load_item()


    # # Get the next 20 listings from 'next page' - persist until no more #
    #     next_page = response.xpath("/.//a[@class='lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE']/@href").get()
    #     if next_page:
    #         yield response.follow(url=next_page, callback=self.parse)


# main driver
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(YelpSpider)
    process.start()
