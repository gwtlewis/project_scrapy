import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from jd_computer.items import JdComputerItem


class CoumputerSpider(CrawlSpider):
    name = "computers"
    start_urls = ['https://list.jd.com/list.html?cat=670,671,672&page=1&delivery=1&trans=1&JL=4_10_0#J_main']
    url = 'https://list.jd.com'

    def parse(self, response):
        item = JdComputerItem()
        selector = Selector(response)
        computers = selector.xpath('//div[@id="plist"]/ul')
        for eachComputer in computers:
            #prd_tmp = eachComputer.xpath('li/div/div/div[2]/div[1]').extract()
            #if prd_tmp:
            #    prd_name = eachComputer.xpath('li/div/div/div[2]/div[1]/div[@class="p-name"]/a/em/text()').extract()
            #    prd_price = eachComputer.xpath('li/div/div/div[2]/div[1]/div[@class="p-price"]'
            #                                   '/strong[@class="J_price"]/i/text()').extract()
            #    prd_img_src = eachComputer.xpath('li/div/div/div[2]/div[1]/div[@class="p-img"]/a/img/@src').extract()
            #    print("DETECTED")
            #else:
            prd_name = eachComputer.xpath('li/div/div[@class="p-name"]/a/em/text()').extract()
            prd_price = eachComputer.xpath('li/div/div[@class="p-price"]/strong[@class="J_price"]/i/text()').extract()
            prd_img_src = eachComputer.xpath('li/div/div[@class="p-img"]/a/img/@src').extract()
            if prd_price:
                prd_price = prd_price[0]
            else:
                prd_price = '0'
            item['prd_name'] = prd_name
            item['prd_price'] = prd_price
            item['prd_img_src'] = prd_img_src
            yield item

        # nextlink = selector.xpath('//a[@class="pn-next"]/@href').extract()

        # if nextlink:
        #    nextlink = nextlink[0]
        #    yield Request(self.url+nextlink, callback=self.parse)
