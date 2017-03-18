# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class SnComputerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    prd_brand = Field()
    prd_name = Field()
    prd_price = Field()
    prd_memory = Field()
    prd_gpu = Field()
    prd_cpu = Field()
    prd_disk = Field()
    prd_type = Field()
    prd_url = Field()
    prd_img = Field()
    good_rate = Field()
    prd_id = Field()
