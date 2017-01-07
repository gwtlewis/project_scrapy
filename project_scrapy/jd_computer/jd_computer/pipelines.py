# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from jd_computer.items import JdComputerItem
from scrapy import log


class JdComputerPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        try:
            db = connection[settings['MONGODB_DB']]
            self.connection = db[settings['MONGODB_COLLECTION']]
            print("MonoDB connection established...")
        except Exception as e:
            print("An exception occurred: "+e.__str__())

    def process_item(self, item, spider):
        computer = dict(item)
        self.connection.insert(computer)
        log.msg("Computers added to MongoDB database", _level=log.INFO, spider=spider)

        return item
