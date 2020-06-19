#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#
#   |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|    #
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#
'''          Spider for Yelp             '''
# 'meta' passes variables between methods  #

import os
import scrapy
import my_classnames # puts classnames into short variables
from scrapy.loader import ItemLoader
from items import YelpItem
from scrapy.crawler import CrawlerProcess
from scrapy import Request

class YelpSpider(scrapy.Spider):

    name = 'yelp-spider'
    custom_settings = {"FEEDS": {"results.csv": {"format": "csv"}},'CONCURRENT_REQUESTS': 1}
    start_urls = ['https://www.yelp.com/search?find_desc=Plumbers&find_loc=London&ns=1']
    headers = {
        'user-agent' :
        'User-Agent: Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
        }

    try:
        os.remove('results.csv')
    except OSError:
        pass

    def start_requests(self):
            # Starting url
            url = 'https://www.yelp.com/search?find_desc=Plumbers&find_loc=London&ns=1'
            # crawl next page URL
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self,response):
        # Iterate through 20 adverts per page
        all_ads =  response.xpath(my_classnames.v_container)
        for ads in all_ads:

            # Get Link to detail page (20 per page)
            link = ads.xpath(my_classnames.v_link)
            # Get link to image logo
            logo_url = ads.xpath(my_classnames.v_logo_url).get()
            # Get Company Name
            lcompanyname = ads.xpath(my_classnames.v_company_name).get()

            link = link.get()
            absolute_url = response.urljoin(link )

            # OLD 'meta' CODE # yield Request(absolute_url, callback=self.fetch_detail, meta={'link': link, 'logo_url': logo_url, 'lcompanyname':lcompanyname})

            request = Request(absolute_url, callback=self.fetch_detail, cb_kwargs={'link': link, 'logo_url': logo_url, 'lcompanyname':lcompanyname})
            yield request

        # # Get the next 20 listings from 'next page' - persist until no more #
        next_page = response.xpath(my_classnames.v_next_page).get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    def fetch_detail(self,response, link, logo_url, lcompanyname):


        # OLD 'meta' code #
        # link = response.meta.get('link')
        # logo_url = response.meta.get('logo_url')
        # lcompanyname = response.meta.get('lcompanyname')
        #
        co_website = response.xpath(my_classnames.v_co_website).get() # website //text()').get()
        co_tel = response.xpath(my_classnames.v_co_tel).getall()[1] # TEL No.

        yield{'lcompany_name' : lcompanyname, 'co_website':co_website, 'co_tel': co_tel, 'logo_url' : logo_url, 'link':link}

        # l = ItemLoader(item=YelpItem(), response=response)
        # loader.add_value("link",link)
        # loader.add_value("logo_url",logo_url)
        # loader.add_value("lcompanyname",lcompanyname)
        # loader.add_value("co_website",co_website)
        # loader.add_value("co_tel",co_tel)
        # yield l.load_item()

# main driver
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(YelpSpider)
    process.start()
