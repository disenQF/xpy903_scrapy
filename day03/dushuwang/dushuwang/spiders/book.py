# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['www.dushu.com', 'pic.dushu.com', 'img.dushu.com']
    start_urls = ['https://www.dushu.com/book/']

    rules = (
        # 分类下的图片列表
        Rule(LinkExtractor(allow=r'/book/\d+\.html'), follow=True),

        # https://www.dushu.com/book/13491825/  详情
        Rule(LinkExtractor(allow=r'/book/\d+/'),
             callback='parse_item',
             follow=False),

        # 分页的规则
        Rule(LinkExtractor(allow=r'/book/\d+_\d+\.html'), follow=True),

    )

    def parse_item(self, response):
        # 解析图书详情页面的
        i = {}
        # 书名
        i['name'] = response.css('h1::text').get()
        i['cover_url'] = response.css('.book-pic img').xpath('./@src').get()
        i['price'] = response.css('.price span::text').get()

        book_info_div = response.css('.book-details-left')
        i['author'] = book_info_div.xpath('.//tr[1]/td[2]/text()').get()
        i['publisher'] = book_info_div.xpath('.//tr[2]/td[2]//text()').get()
        i['labels'] = book_info_div.xpath('.//tr[4]/td[2]/text()').get()

        table = response.css('.book-details>table')
        i['ISBN'] = table.xpath('.//tr[1]/td[2]/text()').get()
        i['publish_time'] = table.xpath('.//tr[1]/td[4]/text()').get()
        i['pages'] = table.xpath('.//tr[2]/td[4]/text()').get()

        return i
