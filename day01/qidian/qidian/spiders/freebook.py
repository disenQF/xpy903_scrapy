# -*- coding: utf-8 -*-
import uuid

import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse


class FreebookSpider(scrapy.Spider):
    name = 'freebook'
    allowed_domains = ['www.qidan.com', 'book.qidian.com', 'read.qidian.com']
    start_urls = ['https://www.qidian.com/free/all']

    def parse(self, response: HtmlResponse):
        # 解析开始页面的响应数据
        # response-> scrapy.http.HtmlResponse
        if response.status == 200:
            # print(response.text)
            li_nodes = response.css('.all-img-list li')  # list[<Selector>, ..]
            # print(type(li_nodes))
            # print(li_nodes)
            for index, li_node in enumerate(li_nodes):
                # 查看每本书的信息
                item = {}
                # item['name'] = li_node.css('h4 a').xpath('./text()').extract_first()
                item['name'] = li_node.css('h4 a::text').get()
                item['author'] = li_node.css('.name::text').get()

                # info_url = css('.book-img-box a::attr("href")').get()
                item['info_url'], item['cover_url'] = li_node.css('.book-img-box a').xpath(
                    './@href | ./img/@src').extract()
                item['tags'] = li_node.css('.author').xpath('./a[position()>1]/text() | ./span/text()').extract()
                item['summary'] = li_node.css('.intro::text').extract_first()  # p标签的文本信息
                item['id'] = uuid.uuid4().hex


                # 将数据回传给引擎engine
                yield item

                # 发起查看详情的请求（由engine压入到scheduler中）
                yield Request('https:' + item['info_url'],
                              callback=self.parse_detail,
                              meta={'book_id': item['id']},
                              priority=200-index)  # 请求在scheduler中的优先级，值越大级别越高。

            # 下一页
            next_url = response.css('.lbf-pagination-item-list').xpath('./li[last()]/a/@href').get()
            # 发起下一页的请求
            if next_url.find('javascript') == -1:
                yield Request('https:' + next_url, dont_filter=True, priority=10)

    def parse_detail(self, response):
        # 图书详情
        print('-'*20, '开始阅读', sep='\n')
        chap_url = 'https:'+response.css('.red-btn').xpath('./@href').get()

        print('-'*20+chap_url+'-'*10)

        yield Request(chap_url,
                      callback=self.parse_chapter,
                      meta={'book_id': response.request.meta['book_id']},
                      priority=500)

    def parse_chapter(self, response):
        item = {}
        item['title'] = response.css('.content-wrap::text').get()
        item['contents'] = response.css('.read-content p::text').extract()
        item['book_id'] = response.request.meta['book_id']

        yield item

        # 下一章节


