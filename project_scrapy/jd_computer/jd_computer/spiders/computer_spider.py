# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from jd_computer.items import JdComputerItem
from pymongo import MongoClient


class CoumputerSpider(CrawlSpider):
    name = "computers"

    client = MongoClient(host="118.89.48.117", port=27027)
    db = client['Douban']
    db.authenticate(name="dbOwner", password="Db1419")
    collection = db['jd_com_urls']

    url_list = []
    for url in collection.find({}):
        url_list.append(url['url'].encode("utf-8"))

    i = 2
    start_urls = [url_list[i]]
    allowed_domains = ["jd.com"]

    comparable = [1, 35, 82, 14, 11, 43, 29, 9, 63, 97, 41, 44, 57, 73, 72, 84]

    def parse(self, response):
        item = JdComputerItem()
        selector = Selector(response)
        prd_price = selector.xpath('//div[@class="summary-price J-summary-price"]/div[2]/span/span[2]/text()').extract()
        prd_details = selector.xpath('/html/body/div/div[@class="detail"]/div[@class="ETab"]/div[@class="tab-con"]/div[1]/div[1]')
        prd_brand = prd_details.xpath('ul[1]/li/@title').extract()
        item['prd_id'] = self.i+1
        item['prd_seller'] = 'jd'
        if (self.i + 1) in self.comparable:
            item['comparable'] = True
        else:
            item['comparable'] = False
        if prd_price:
            item['prd_price'] = prd_price[0]
            item['prd_brand'] = prd_brand[0]
            item['prd_name'] = prd_details.xpath('/html/body/div[5]/div/div[2]/div[1]/text()').extract()[0].replace(" ", "").replace("\n", "")
            item['prd_memory'] = prd_details.xpath(u'ul[2]/li[contains(text(), "内存")]/@title').extract()[0]
            item['prd_cpu'] = prd_details.xpath(u'ul[2]/li[contains(text(), "处理器")]/@title').extract()[0]
            item['prd_gpu'] = prd_details.xpath(u'ul[2]/li[contains(text(), "显卡")]/@title').extract()[0]
            item['prd_disk'] = prd_details.xpath(u'ul[2]/li[contains(text(), "硬盘")]/@title').extract()[0]
            item['prd_url'] = self.url_list[self.i]
            item['prd_img'] = 'https:' + selector.xpath('//div[@class="preview"]/div/img/@src').extract()[0]
            if prd_details.xpath(u'ul[2]/li[contains(text(), "分类")]/@title').extract():
                item['prd_type'] = prd_details.xpath(u'ul[2]/li[contains(text(), "分类")]/@title').extract()[0]
            else:
                item['prd_type'] = '无'
            item['good_rate'] = selector.xpath('//*[@id="comment"]/div[2]/div[1]/div[1]/div/text()').extract()[
                                    0] + '%'
        else:
            prd_price = selector.xpath('//div[@class="summary-price J-summary-price"]/div/div/span/span/span[2]/text()').extract()
            if prd_price:
                item['prd_price'] = prd_price[0]
                item['prd_brand'] = prd_brand[0]
                item['prd_name'] = prd_details.xpath('/html/body/div[5]/div/div[2]/div[1]/text()').extract()[0].replace(" ", "").replace("\n", "")
                item['prd_memory'] = prd_details.xpath(u'ul[2]/li[contains(text(), "内存")]/@title').extract()[0]
                item['prd_cpu'] = prd_details.xpath(u'ul[2]/li[contains(text(), "处理器")]/@title').extract()[0]
                item['prd_gpu'] = prd_details.xpath(u'ul[2]/li[contains(text(), "显卡")]/@title').extract()[0]
                item['prd_disk'] = prd_details.xpath(u'ul[2]/li[contains(text(), "硬盘")]/@title').extract()[0]
                item['prd_url'] = self.url_list[self.i]
                item['prd_img'] = 'https:' + selector.xpath('//div[@class="preview"]/div/img/@src').extract()[0]
                if prd_details.xpath(u'ul[2]/li[contains(text(), "分类")]/@title').extract():
                    item['prd_type'] = prd_details.xpath(u'ul[2]/li[contains(text(), "分类")]/@title').extract()[0]
                else:
                    item['prd_type'] = '无'
                item['good_rate'] = selector.xpath('//*[@id="comment"]/div[2]/div[1]/div[1]/div/text()').extract()[
                                        0] + '%'
            else:
                item['prd_price'] = '0'
                item['prd_brand'] = '0'
                item['prd_name'] = '0'
                item['prd_memory'] = '0'
                item['prd_cpu'] = '0'
                item['prd_gpu'] = '0'
                item['prd_disk'] = '0'
                item['prd_url'] = '0'
                item['prd_img'] = '0'
                item['prd_type'] = '0'
                item['good_rate'] = '0'
        yield item

        self.i += 1
        if self.i <= 99:
            yield Request(url=self.url_list[self.i], callback=self.parse)

        # start_urls = ['https://list.jd.com/list.html?cat=670,671,672&page=1&delivery=1&trans=1&JL=4_10_0#J_main']
        # computers = selector.xpath('//div[@id="plist"]/ul/li/div')
        # for eachComputer in computers:
        #     prd_name = eachComputer.xpath('div[@class="p-name"]/a/em/text()').extract()
        #     if prd_name:
        #         prd_sku = eachComputer.xpath('@data-sku').extract()
        #         prd_price = eachComputer.xpath('div[@class="p-price"]/strong[@class="J_price"]/i/text()').extract()
        #         prd_img_src = eachComputer.xpath('div[@class="p-img"]/a/img/@src').extract()
        #         prd_url = eachComputer.xpath('div[@class="p-name"]/a/@href').extract()
        #     else:
        #         prd_sku = eachComputer.xpath('div/div[2]/div[1]/@data-sku').extract()
        #         prd_name = eachComputer.xpath('div/div[2]/div[1]/div[@class="p-name"]/a/em/text()').extract()
        #         prd_price = eachComputer.xpath('div/div[2]/div[1]/div[@class="p-price"]/strong[@class="J_price"]/i/'
        #                                        'text()').extract()
        #         prd_img_src = eachComputer.xpath('div/div[2]/div[1]/div[@class="p-img"]/a/img/@src').extract()
        #         prd_url = eachComputer.xpath('div/div[2]/div[1]/div[@class="p-name"]/a/@href').extract()
        #     item['prd_img_src'] = 'https:'+prd_img_src[0]
        #     item['prd_name'] = prd_name[0]
        #     item['prd_sku'] = prd_sku[0]
        #     item['prd_price'] = prd_price[0]
        #     item['prd_url'] = 'https:'+prd_url[0]
        #      yield item#
        #    nextlink = selector.xpath('//a[@class="pn-next"]/@href').extract()
        #    if nextlink:
        #        nextlink = nextlink[0]
        #        yield Request(self.url+nextlink, callback=self.parse)