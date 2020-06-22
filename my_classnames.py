#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#
#   |r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|    #
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#
'''          Spider for Yelp             '''
# 'meta' passes variables between methods  #
# verbose classnames -> variables

v_container = '//*[@class="lemon--div__373c0__1mboc container__373c0__3HMKB hoverable__373c0__VqkG7 margin-t3__373c0__1l90z margin-b3__373c0__q1DuY padding-t3__373c0__1gw9E padding-r3__373c0__57InZ padding-b3__373c0__342DA padding-l3__373c0__1scQ0 border--top__373c0__3gXLy border--right__373c0__1n3Iv border--bottom__373c0__3qNtD border--left__373c0__d1B7K border-color--default__373c0__3-ifU"]'

v_link = './/a[@class="lemon--a__373c0__IEZFH link__373c0__1G70M photo-box-link__373c0__1YC9Y link-color--blue-dark__373c0__85-Nu link-size--default__373c0__7tls6"]/@href'
# 'contains'
# can be replaced with ~ response.xpath('//*[contains(@href,"biz")]/@href').getall()[:20]
# eg. 
# v_link = './/*[contains(@href,"biz")]/@href'

v_logo_url = './/img[@class="lemon--img__373c0__3GQUb photo-box-img__373c0__35y5v"]/@src'

v_company_name = './/*[@class="lemon--a__373c0__IEZFH link__373c0__1G70M link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE"]/@name'
# 'contains' ... 'and not'
# can be replaced with ~ response.xpath('//*[contains(@href,"biz") and not (contains(text(),"more"))]/text()').getall()[:20]

v_co_website = '//a[@class="lemon--a__373c0__IEZFH link__373c0__1G70M link-color--blue-dark__373c0__85-Nu link-size--inherit__373c0__1VFlE"]//text()'
v_co_tel = '//p[@class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-"]/text()'
v_next_page = "/.//a[@class='lemon--a__373c0__IEZFH link__373c0__1G70M next-link navigation-button__373c0__23BAT link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE']/@href"

# 'starts-with'
# Find all the Yelp addresses :
# response.xpath("//a[starts-with(@href, 'https://www.yelp')]").getall()

# 'starts-with' ...or...'starts-with' 
# Find hrefs starting with yelp, or official 
# response.xpath("//a[starts-with(@href, 'https://yelp') or starts-with(@href, 'https://official')]").getall()



