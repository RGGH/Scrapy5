#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#
#   |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|    #
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#
'''          Spider for Yelp             '''
# 'meta' passes variables between methods  #

import os
import scrapy
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
        all_ads =  response.xpath('//*[@class="lemon--div__373c0__1mboc container__373c0__3HMKB hoverable__373c0__VqkG7 margin-t3__373c0__1l90z margin-b3__373c0__q1DuY padding-t3__373c0__1gw9E padding-r3__373c0__57InZ padding-b3__373c0__342DA padding-l3__373c0__1scQ0 border--top__373c0__3gXLy border--right__373c0__1n3Iv border--bottom__373c0__3qNtD border--left__373c0__d1B7K border-color--default__373c0__3-ifU"]')
        for ads in all_ads:

            # details_link = same as 'link'
            details_link = ads.xpath(".//a[@class='lemon--a__373c0__IEZFH link__373c0__1G70M photo-box-link__373c0__1YC9Y link-color--blue-dark__373c0__85-Nu link-size--default__373c0__7tls6']/@href").get()
            absolute_url = response.urljoin(details_link )

            # Get Link to detail page (20 per page)
            link = ads.xpath(".//a[@class='lemon--a__373c0__IEZFH link__373c0__1G70M photo-box-link__373c0__1YC9Y link-color--blue-dark__373c0__85-Nu link-size--default__373c0__7tls6']/@href")
            # Get link to image logo (23 at moment)
            logo_url = ads.xpath(".//img[@class='lemon--img__373c0__3GQUb photo-box-img__373c0__35y5v']/@src").get()
            # Get Company Name
            lcompanyname = ads.xpath(".//*[@class='lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE']/@name").get()

            yield Request(absolute_url, callback=self.fetch_detail, meta={'link': link, 'logo_url': logo_url, 'lcompanyname':lcompanyname})

    def fetch_detail(self,response):

        link = response.meta.get('link')
        logo_url = response.meta.get('logo_url')
        lcompanyname = response.meta.get('lcompanyname')
        co_website = response.xpath('//a[@class="lemon--a__373c0__IEZFH link__373c0__1G70M link-color--blue-dark__373c0__85-Nu link-size--inherit__373c0__1VFlE"]//text()').get() # website //text()').get()
        co_tel = response.xpath('//p[@class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-"]/text()').getall()[1] # TEL No.

        yield{'lcompany_name' : lcompanyname, 'co_website':co_website, 'co_tel': co_tel, 'logo_url' : logo_url}


        # l = ItemLoader(item=YelpItem(), response=response)
        # loader.add_value("link",link)
        # loader.add_value("logo_url",logo_url)
        # loader.add_value("lcompanyname",lcompanyname)
        # loader.add_value("co_website",co_website)
        # loader.add_value("co_tel",co_tel)
        # yield l.load_item()

    # uncomment below right at end!!! ____________________________________________________________________________________________________

    # # Get the next 20 listings from 'next page' - persist until no more #
    #     next_page = response.xpath("/.//a[@class='lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE']/@href").get()
    #     if next_page:
    #         yield response.follow(url=next_page, callback=self.parse)

# main driver
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(YelpSpider)
    process.start()
