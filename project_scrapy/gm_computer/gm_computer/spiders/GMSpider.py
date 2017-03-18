# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from gm_computer.items import GmComputerItem
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ComputerSpider(CrawlSpider):
    name = "gm_computers"

    client = MongoClient(host="118.89.48.117", port=27027)
    db = client['Douban']
    db.authenticate(name="dbOwner", password="Db1419")
    collection = db['gm_com_urls']

    url_list = []
    for url in collection.find({}):
        url_list.append(url['url'].encode("utf-8"))

    i = 0
    start_urls = [url_list[i]]
    allowed_domains = ["gome.com.cn"]

    comparable = [1, 23, 29, 37, 6, 7, 34, 48, 74, 90, 45, 88, 99, 2, 28, 84]

    def parse(self, response):
        item = GmComputerItem()
        selector = Selector(response)
        item['prd_seller'] = 'gm'
        if (self.i + 1) in self.comparable:
            item['compaarable'] = True
        else:
            item['compaarable'] = False
        item['prd_brand'] = selector.xpath(u'//*[@id="prd_data"]/li[2]/ul[1]/li/span[contains(text(), "品牌")]/'
                                           u'../span[2]/text()').extract()[0]
        item['prd_name'] = selector.xpath('//*[@id="prd_data"]/li[1]/div[1]/div[1]/@title').extract()[0]
        price_normal = selector.xpath('//*[@id="prdPrice"]/text()').extract()
        item['prd_id'] = self.i + 1
        item['prd_price'] = price_normal[0]
        memory = selector.xpath(u'//*[@id="prd_data"]/li[2]/ul[1]/li/span[contains(text(), "内存")]/../'
                                u'span[2]/text()').extract()
        tmp1 = ''
        if memory:
            for tmp2 in memory:
                tmp1 += tmp2 + ' '
            item['prd_memory'] = tmp1
        else:
            item['prd_memory'] = 'unknown'
        gpu = selector.xpath(u'//*[@id="prd_data"]/li[2]/ul[1]/li/span[contains(text(), "显卡")]/..'
                             u'/span[2]/text()').extract()
        b = ''
        for a in gpu:
            b += a+' '
        item['prd_gpu'] = b
        cpu = selector.xpath('//*[@id="prd_data"]/li[2]/ul[1]/li/span[contains(text(), "CPU")]/'
                             '../span[2]/text()').extract()
        cpu2 = selector.xpath(u'//*[@id="prd_data"]/li[2]/ul[1]/li/span[contains(text(), "处理器")]/'
                              u'../span[2]/text()').extract()
        if cpu:
            item['prd_cpu'] = cpu[0]
        elif cpu2:
            item['prd_cpu'] = cpu2[0]
        else:
            item['prd_cpu'] = 'unknown'
        item['prd_disk'] = selector.xpath(u'//*[@id="prd_data"]/li[2]/ul[1]/li/span[contains(text(), "硬盘")]/'
                                          u'../span[2]/text()').extract()[0]
        type = selector.xpath(u'//*[@id="prd_data"]/li[2]/ul[1]/li/span[contains(text(), "适用")]/../span[2]/text()').extract()
        if type:
            item['prd_type'] = type[0]
        item['prd_url'] = self.url_list[self.i]
        item['prd_img'] = 'http:' + selector.xpath('//*[@id="gm-main-info"]/div[1]/div[1]/div[1]/div/img/@src').extract()[0]
        item['good_rate'] = selector.xpath('//*[@id="j-comment-section"]/div/div[1]/div[1]/div[1]/span/text()').extract()[0] + '%'
        yield item

        self.i += 1
        if self.i <= 99:
            yield Request(url=self.url_list[self.i], callback=self.parse)
