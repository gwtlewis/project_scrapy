# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from gm_computer.items import DemoItem # 如果Pycharm出现红线，忽略即可


"""
设置页面编码
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ComputerSpider(CrawlSpider):
    name = "demo"
    start_urls = ["https://my.oschina.net/lewisgong"]
    allowed_domains = ["oschina.net"] # 允许访问的域名，如果访问的页面不是在该域名下，则爬虫终止

    def parse(self, response):
        """
        处理页面数据
        """
        item = DemoItem()
        selector = Selector(response)

        item['demo'] = selector.xpath('xpath of element').extract()[0]

        yield item

        if True: # 判断是否有下一页，条件自己定义
            yield Request(url="下一页的地址", callback=self.parse) # 将下一页的地址传回parse()继续抓取数据
