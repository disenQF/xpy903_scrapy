# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 处理解析之后的数据
# 【注】声明的pipeline类必须注册到settings.py中
from qidian.items import BookItem


class QidianPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            print('------将book数据存放到mysql-----')

        else:
            print('------将chapter数据存放到mysql-----')

        return item  # 返回item-可以被其它等级低的pipeline处理


class ESPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            print('------将book数据存放到es-----')

        else:
            print('------将chapter数据存放到es-----')

        return item