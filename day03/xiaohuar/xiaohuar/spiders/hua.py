# -*- coding: utf-8 -*-
import scrapy


class HuaSpider(scrapy.Spider):
    name = 'hua'
    allowed_domains = ['www.xiaohuar.com']
    start_urls = ['http://www.xiaohuar.com/hua/']

    def parse(self, response):
        for item_t in response.css('.item_t'):
            info_url = item_t.css('.img a::attr("href")').get()
            yield scrapy.Request(info_url, priority=100, callback=self.parse_info)

        # 下一页的url
        next_page_url = response.css('.page_num a:nth-last-child(2)::attr("href")').get()
        yield scrapy.Request(next_page_url)

    def parse_info(self, response):
        item = {}
        info_div = response.css('.infodiv')
        item['name'] = info_div.xpath('.//tr[1]/td[2]/text()').get()
        item['age'] = info_div.xpath('.//tr[2]/td[2]/text()').get()
        item['star_info'] = info_div.xpath('.//tr[3]/td[2]/text()').get()
        item['zy_info'] = info_div.xpath('.//tr[4]/td[2]/text()').get()
        item['school'] = info_div.xpath('.//tr[5]/td[2]/text()').get()
        item['post_info'] = info_div.xpath('.//tr[6]/td[2]/text()').get()

        item['detail'] = response.css('.infocontent').xpath('.//span/text()').extract()
        item['detail'] = list(map(lambda item: item.replace('\xa0', ''),
                                  item['detail']))

        item['image_urls'] = response.css('.photo_ul img').xpath('./@src').extract()
        item['image_urls'] = list(map(
            lambda item: "http://www.xiaohuar.com"+item,
            item['image_urls']
        ))

        yield item
