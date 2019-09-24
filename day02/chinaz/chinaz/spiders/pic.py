# -*- coding: utf-8 -*-
import scrapy


class PicSpider(scrapy.Spider):
    name = 'pic'
    allowed_domains = ['sc.chinaz.com',
                       'pic.sc.chinaz.com',
                       'pic2.sc.chinaz.com']
    start_urls = ['http://sc.chinaz.com/tupian/']

    base_url = 'http://sc.chinaz.com/tupian/'

    def parse(self, response):

        for div in response.css('#container div'):
            name = div.xpath('./p/a/text()').get()
            cover_url = div.css('img::attr("src2")').get()

            yield {
                'name': name,
                'image_urls': [cover_url],
                'images': '',
            }

        # 下一页
        next_page_url = response.css('.nextpage::attr("href")').get()
        yield scrapy.Request(self.base_url+next_page_url)
