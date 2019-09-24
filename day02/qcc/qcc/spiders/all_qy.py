# -*- coding: utf-8 -*-
import scrapy


class AllQySpider(scrapy.Spider):
    name = 'all_qy'
    allowed_domains = ['www.qichacha.com']
    start_urls = ['https://www.qichacha.com/g_AH.html']

    base_url = 'https://www.qichacha.com'

    def parse(self, response):
        # 获取所有的地区province企业列表的首页
        if response.url == 'https://www.qichacha.com/g_AH.html':
            qy_urls = response.css('.pills-after')[0].css('a::attr("href")').extract()
            for p_url in qy_urls:
                yield scrapy.Request(self.base_url+p_url, priority=10)

        # 从列表中获取当前企业的详情页面的url
        for tr_ in response.css('.m_srchList tr'):
            info_url = tr_.css('td:nth-child(2) a::attr("href")').get()
            yield scrapy.Request(self.base_url+info_url,
                                 callback=self.parse_detail,
                                 priority=100)

        # 获取当前地区的下一页url
        next_url = response.css('.next::attr("href")').get()
        yield scrapy.Request(self.base_url+next_url, priority=50)

    def parse_detail(self, response):
        #  企业名称、电话、地址、运营状态（注销/吊销、在业、存续）、
        #  成立时间、纳税人识别号、经营者、统一社会信用代码、所属地区
        #  经营范围
        pass

