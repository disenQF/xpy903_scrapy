# -*- coding: utf-8 -*-
import scrapy


class AllQySpider(scrapy.Spider):
    name = 'all_qy'
    allowed_domains = ['www.qichacha.com']
    start_urls = ['https://www.qichacha.com/g_AH.html']

    base_url = 'https://www.qichacha.com'

    def parse(self, response):

        # 从列表中获取当前企业的详情页面的url
        for tr_ in response.css('.m_srchList tr'):
            info_url = tr_.css('td:nth-child(2) a::attr("href")').get()
            yield scrapy.Request(self.base_url+info_url,
                                 callback=self.parse_detail,
                                 priority=100)

        # 获取所有的地区province企业列表的首页
        if response.url == 'https://www.qichacha.com/g_AH.html':
            qy_urls = response.xpath('//div[@class="pills-after" and position()=1]').css('a::attr("href")').extract()
            if qy_urls:
                for p_url in qy_urls:
                    yield scrapy.Request(self.base_url+p_url, priority=10)


        # 获取当前地区的下一页url
        next_url = response.css('.next::attr("href")').get()
        yield scrapy.Request(self.base_url+next_url, priority=50)

    def parse_detail(self, response):
        #  企业名称、电话、地址、运营状态（注销/吊销、在业、存续）、
        #  成立时间、纳税人识别号、统一社会信用代码、经营者、所属地区
        #  经营范围
        name = response.css('h1::text').get()
        phone, *_, address = response.css('.cvlu::text').extract()
        status = response.css('.tags span::text').get()

        regist_time = response.css('#Cominfo').xpath('.//tr[3]//td[4]/text()').get()
        # 识别码
        code = response.css('#Cominfo').xpath('.//tr[4]//td[4]/text()').get()

        # 信用代码
        code2 = response.css('#Cominfo').xpath('.//tr[4]//td[2]/text()').get()

        user_name = response.css('.boss-td h2::text').get()

        province = response.css('#Cominfo').xpath('.//tr[8]//td[2]/text()').get()
        content = response.css('#Cominfo').xpath('.//tr[last()]//td[2]/text()').get()

        return dict(
            name=name,
            phone=phone,
            address=address,
            status=status,
            regist_time=regist_time,
            code=code,
            code2=code2,
            user_name=user_name,
            province=province,
            content=content
        )








