# -*- coding: utf-8 -*-
import scrapy
from dushuwang.ydm import ydm_api

class CollectSpider(scrapy.Spider):
    name = 'collect'
    allowed_domains = ['www.gushiwen.org', 'so.gushiwen.org']

    def start_requests(self):
        # 爬虫开始位置
        code_url = 'https://so.gushiwen.org/RandCode.ashx'
        yield scrapy.Request(code_url, callback=self.parse_code)

    def parse_code(self,response):
        login_url = 'https://so.gushiwen.org/user/login.aspx'

        with open('code.png', 'wb') as f:
            f.write(response.body)

        code = ydm_api('code.png')

        yield scrapy.FormRequest(login_url,
                                 formdata={
                                     'email':'610039018@qq.com',
                                     'pwd': 'disen8888',
                                     'code': code
                                 }, callback=self.parse)

    def parse(self, response):
        # 解析收藏页面的内容
        with open('collect.html', 'wb') as f:
            f.write(response.body)

