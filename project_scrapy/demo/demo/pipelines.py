# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
import pymongo
from scrapy.conf import settings


class DemoPipeline(object):
    def __init__(self):
        try:
            connection = pymongo.MongoClient(host=settings['MONGODB_SERVER'], port=settings['MONGODB_PORT'])
            db = connection[settings['MONGODB_DB']]
            db.authenticate(name=settings['MONGODB_USER'], password=settings['MONGODB_PWD'])
            self.connection = db[settings['MONGODB_COLLECTION']]
            print("MonoDB connection established...")
        except Exception as e:
            print("An exception occurred when try to connect to MongoDB: "+str(e))

    def process_item(self, item, spider):
        computer = dict(item)
        self.connection.insert(computer)
        log.msg("Computers added to MongoDB database", _level=log.INFO, spider=spider)

        return item