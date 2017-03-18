# -*- coding: utf-8 -*-

import pymongo
import requests

class ComputerLinks(object):
    # client = pymongo.MongoClient(host="118.89.48.117", port=27027)
    # db = client['Douban']
    # db.authenticate(name="dbOwner", password="Db1419")
    # collection = db['jd_computers_20170226']#

    # print list
    # demo = ""
    # for item in list:
    #    if item.startswith('2'):
    #        tmp = item
    #        del item
    #        tmp.replace('2', 'A')
    #        list.append(tmp)#
    # print list

    # for doc in collection.find():
    #     print doc['url']#
    def updateDB(self):
        client = pymongo.MongoClient(host="118.89.48.117", port=27027)
        db = client['Douban']
        db.authenticate(name="dbOwner", password="Db1419")
        collection1 = db['gm_computers_20170313']
        collection2 = db['_gm_computers_20170313']
        record = collection2.find()
        collection1.insert_many(record)

if __name__ == "__main__":
    comp = ComputerLinks()
    print comp.updateDB()

