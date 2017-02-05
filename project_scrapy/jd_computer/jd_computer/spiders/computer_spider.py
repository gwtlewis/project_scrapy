import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from jd_computer.items import JdComputerItem


class CoumputerSpider(CrawlSpider):
    name = "computers"
    start_urls = ['https://list.jd.com/list.html?cat=670,671,672&page=1&delivery=1&trans=1&JL=4_10_0#J_main']
    allowed_domains = ["jd.com"]
    url = 'https://list.jd.com'

    def parse(self, response):
        item = JdComputerItem()
        selector = Selector(response)
        computers = selector.xpath('//div[@id="plist"]/ul/li/div')
        for eachComputer in computers:
            prd_name = eachComputer.xpath('div[@class="p-name"]/a/em/text()').extract()
            if prd_name:
                prd_sku = eachComputer.xpath('@data-sku').extract()
                prd_price = eachComputer.xpath('div[@class="p-price"]/strong[@class="J_price"]/i/text()').extract()
                prd_img_src = eachComputer.xpath('div[@class="p-img"]/a/img/@src').extract()
                prd_url = eachComputer.xpath('div[@class="p-name"]/a/@href').extract()
            else:
                prd_sku = eachComputer.xpath('div/div[2]/div[1]/@data-sku').extract()
                prd_name = eachComputer.xpath('div/div[2]/div[1]/div[@class="p-name"]/a/em/text()').extract()
                prd_price = eachComputer.xpath('div/div[2]/div[1]/div[@class="p-price"]/strong[@class="J_price"]/i/'
                                               'text()').extract()
                prd_img_src = eachComputer.xpath('div/div[2]/div[1]/div[@class="p-img"]/a/img/@src').extract()
                prd_url = eachComputer.xpath('div/div[2]/div[1]/div[@class="p-name"]/a/@href').extract()
            item['prd_img_src'] = 'https:'+prd_img_src[0]
            item['prd_name'] = prd_name[0]
            item['prd_sku'] = prd_sku[0]
            item['prd_price'] = prd_price[0]
            item['prd_url'] = 'https:'+prd_url[0]
            yield item

            nextlink = selector.xpath('//a[@class="pn-next"]/@href').extract()
            if nextlink:
               nextlink = nextlink[0]
               yield Request(self.url+nextlink, callback=self.parse)
