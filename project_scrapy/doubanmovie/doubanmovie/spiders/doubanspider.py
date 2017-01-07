import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from doubanmovie.items import DoubanmovieItem


class Douban (CrawlSpider):
    name = "douban"
    start_urls = ['https://movie.douban.com/top250']

    url = 'https://movie.douban.com/top250'

    def parse(self, response):
        item = DoubanmovieItem()
        selector = Selector(response)
        movies = selector.xpath('//div[@class="info"]')
        for eachMovie in movies:
            title = eachMovie.xpath('div[@class="hd"]/a/span/text()').extract()
            fulltitle = ''
            for each in title:
                fulltitle += each
            movieInfo = eachMovie.xpath('div[@class="bd"]/p/text()').extract()
            star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            quote =eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['title'] = fulltitle
            item['movieInfo'] = ';'.join(movieInfo)
            item['star'] = star
            item['quote'] = quote
            yield item

        nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()

        if nextLink:
            nextLink = nextLink[0]
            print(nextLink)
            yield Request(self.url+nextLink, callback=self.parse)

