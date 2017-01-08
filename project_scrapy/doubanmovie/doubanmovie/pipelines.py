# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy import log
from items import DoubanmovieItem


class DoubanmoviePipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        connection.admin.authenticate(settings['MONGODB_USER'], settings['MONGODB_PSW'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        movie = dict(item)
        self.collection.insert(movie)
        log.msg("Movies added to MongoDB database", _level=log.INFO, spider=spider)

        return item
