from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from get_jd_computer_link.items import GetJdComputerLinkItem


class GetComputerLinks(CrawlSpider):
    name = "ComputerLinksSpider"
    start_urls = ['https://list.jd.com/list.html?cat=670,671,672&page=1&delivery=1&trans=1&JL=4_10_0#J_main']
    allowed_domains = ["jd.com"]
    url = 'https://list.jd.com'

    def parse(self, response):
        item = GetJdComputerLinkItem()
        selector = Selector(response)
        computerLinks = selector.xpath('//div[@id="plist"]/ul/li/div')
        for eachComputerLinks in computerLinks:
            prd_name = eachComputerLinks.xpath('div[@class="p-name"]/a/em/text()').extract()
            if prd_name:
                computer_link = eachComputerLinks.xpath('div[@class="p-name"]/a/@href').extract()
            else:
                computer_link = eachComputerLinks.xpath('div/div[2]/div[1]/div[@class="p-name"]/a/@href').extract()
            item['computer_link'] = 'https'+computer_link[0]

            yield item

            nextlink = selector.xpath('//a[@class="pn-next"]/@href').extract()
            if nextlink:
                nextlink = nextlink[0]
                yield Request(self.url + nextlink, callback=self.parse)