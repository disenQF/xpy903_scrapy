# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from scrapy_redis.spiders import RedisCrawlSpider


class BookRedisSpider(RedisCrawlSpider):
    name = 'book_redis'
    allowed_domains = ['www.dushu.com']

    redis_key = 'dushu-book:start_urls'  # 可以指定任何有意义的名称

    rules = [
        Rule(LinkExtractor(restrict_css=('.sub-catalog', '.pages')), follow=True),
        Rule(LinkExtractor(restrict_css='.bookslist'), callback='parse_book', follow=False)
    ]

    def parse_book(self, response):
        i = {}
        i['name'] = response.css('.book-title h1::text').get()
        i['price'] = response.css('.price span::text').get()
        i['author'] = response.css('.book-details-left>table').xpath('./tr[1]/td[2]/text()').get()

        yield i
