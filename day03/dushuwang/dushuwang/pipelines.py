# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import uuid


class DushuwangPipeline(object):
    def process_item(self, item, spider):
        spider.logger.info(str(item))

        # name,cover_url,price,author,publisher,
        # labels,ISBN,publish_time,pages

        item['id'] = uuid.uuid4().hex

        insert_sql = 'insert into book(%s) values(%s)' % (
            ','.join([key for key in item]),
            ','.join(['%%(%s)s' % key for key in item])
        )

        print(insert_sql)

        with spider.db as c:
            c.execute(insert_sql, item)
            if c.rowcount > 0:
                print('添加数据成功')

        return item
