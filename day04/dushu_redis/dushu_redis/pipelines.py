# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import uuid


class DushuRedisPipeline(object):
    items = []

    def process_item(self, item, spider):

        # 将item写入到mongodb库中
        item['_id'] = uuid.uuid4().hex

        self.items.append(item)

        # 每100个item写入库中
        if len(self.items) == 100:
            spider.mongo_books.book.insert(self.items)
            self.items = []

        return item
