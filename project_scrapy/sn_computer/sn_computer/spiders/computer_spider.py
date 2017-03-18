# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from sn_computer.items import SnComputerItem
from pymongo import MongoClient


class ComputerSpider(CrawlSpider):
    name = 'sn_computers'

    client = MongoClient(host="118.89.48.117", port=27027)
    db = client['Douban']
    db.authenticate(name="dbOwner", password="Db1419")
    collection = db['sn_com_urls']

    url_list = []
    for url in collection.find({}):
        url_list.append(url['url'].encode("utf-8"))

    i = 0
    start_urls = [url_list[0]]
    allowed_domains = ["suning.com"]

    def parse(self, response):
        item = SnComputerItem()
        selector = Selector(response)
        item['prd_id'] = self.i+1
        item['prd_price'] = selector.xpath('//*[@id="mainPrice"]//span[@class="mainprice"]/text()').extract()[0] + '00'
        item['prd_brand'] = selector.xpath('/html/body/div[5]/div/div[3]/span/a/text()').extract()[0]
        item['prd_img'] = str(selector.xpath('//*[@id="bigImg"]/img/@src').extract()[0]).replace('//', '')
        item['prd_url'] = self.url_list[self.i]
        prd_details = selector.xpath('//*[@id="itemParameter"]/tbody')
        item['prd_name'] = prd_details.xpath(u'tr//span[contains(text(), "名称")]/../../../td[2]/text()').extract()[0]
        item['prd_memory'] = prd_details.xpath(u'tr//span[contains(text(), "内存容量")]/../../../td[2]/text()').extract()[0]
        item['prd_gpu'] = prd_details.xpath(u'tr//span[contains(text(), "显卡型号")]/../../../td[2]/text()').extract()[0]
        item['prd_cpu'] = prd_details.xpath(u'tr//span[contains(text(), "CPU型号")]/../../../td[2]/text()').extract()[0]
        item['prd_disk'] = prd_details.xpath(u'tr//span[contains(text(), "硬盘容量")]/../../../td[2]/text()').extract()[0]
        item['prd_type'] = prd_details.xpath(u'tr//span[contains(text(), "定位")]/../../../td[2]/text()').extract()[0]
        item['good_rate'] = str(selector.xpath('//*[@id="appraise"]/div[1]/div[2]/div[1]/div[1]/'
                                               'div[1]/div/p[1]/span/text()').extract()[0])+'%'
        yield item

        self.i += 1
        if self.i <= 99:
            yield Request(url=self.url_list[self.i], callback=self.parse)
