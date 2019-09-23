# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse


class FreebookSpider(scrapy.Spider):
    name = 'freebook'
    allowed_domains = ['qidan.com']
    start_urls = ['https://www.qidian.com/free/all']

    def parse(self, response: HtmlResponse):
        # 解析开始页面的响应数据
        # response-> scrapy.http.HtmlResponse
        if response.status == 200:
            # print(response.text)
            li_nodes = response.css('.all-img-list li')  # list[<Selector>, ..]
            # print(type(li_nodes))
            # print(li_nodes)
            for li_node in li_nodes:
                # 查看每本书的信息
                item = {}
                # item['name'] = li_node.css('h4 a').xpath('./text()').extract_first()
                item['name'] = li_node.css('h4 a::text').get()
                item['author'] = li_node.css('.name::text').get()

                # info_url = css('.book-img-box a::attr("href")').get()
                item['info_url'], item['cover_url'] = li_node.css('.book-img-box a').xpath('./@href | ./img/@src').extract()
                item['tags'] = li_node.css('.author').xpath('./a[position()>1]/text() | ./span/text()').extract()
                item['summary'] = li_node.css('.intro::text').extract_first()  # p标签的文本信息

                # 将数据回传给引擎engine
                yield item

            # 下一页
            next_url = response.css('.lbf-pagination-item-list').xpath('./li[last()]/a/@href').get()
            # 发起下一页的请求
            yield Request('https:'+next_url, dont_filter=True)


    def parse_detail(self, response):
        pass
