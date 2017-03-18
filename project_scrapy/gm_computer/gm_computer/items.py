# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class GmComputerItem(Item):
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
    prd_seller = Field()
    comparable = Field()
