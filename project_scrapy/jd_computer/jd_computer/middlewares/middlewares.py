# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.support import ui
from scrapy.http import HtmlResponse
import time


class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == "computers":
            driver = webdriver.PhantomJS()  # 指定浏览器
            wait = ui.WebDriverWait(driver, 15)
            print ("PhantomJS is starting...")
            driver.set_window_size(1000, 10000)
            driver.get(request.url)
            js1 = "var q=document.documentElement.scrollTop=5000"
            driver.execute_script(js1)  # 模仿用户操作
            time.sleep(1)
            wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="detail"]/div[1]/ul/li[5]'))
            driver.find_element_by_xpath('//*[@id="detail"]/div[1]/ul/li[5]').click()
            wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="comment"]/div[2]/div[1]/div[1]/div'))
            body = driver.page_source
            print ("The PhantomJS is visiting "+request.url)
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
            driver.close()
            print ("PhantomJS closed")
        else:
            return


class JdComputerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
