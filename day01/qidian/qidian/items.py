# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
# 小说信息类
class BookItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    info_url = scrapy.Field()
    cover_url = scrapy.Field()
    tags = scrapy.Field()
    summary = scrapy.Field()
    id = scrapy.Field()


# 小说的章节信息类
class ChapterItem(scrapy.Item):
    title = scrapy.Field()
    contents = scrapy.Field()
    book_id = scrapy.Field()




