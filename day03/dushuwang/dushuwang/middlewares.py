# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import pymysql
from scrapy import signals

from dushuwang import settings


class DushuwangSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        # 添加日志处理器
        # s.logger.logger.add_handler()

        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

        # 添加数据库连接对象
        spider.db = pymysql.Connect(**settings.DB_CONFIG)

        # 初始化创建表
        # name,cover_url,price,author,publisher,
        # labels,ISBN,publish_time,pages
        select_exist_table = """
            select count(*) as cnt from information_schema.tables
            where table_schema='mes'
            and table_name='book';
        """

        create_sql = """
            create table book(
               id varchar(32) primary key, 
               name varchar(50),
               cover_url VARCHAR(200),
               price VARCHAR(10),
               author VARCHAR(50),
               publisher VARCHAR(50),
               labels VARCHAR(50),
               ISBN   VARCHAR(50),
               publish_time VARCHAR(50),
               pages VARCHAR(6)
            )
        """
        with spider.db as c:
            c.execute(select_exist_table)
            result = c.fetchone()
            print('---book表是否存在mes库中---', result)
            if result['cnt'] == 0:
                c.execute(create_sql)


    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s' % spider.name)

        # 关闭数据库连接
        spider.db.close()

class DushuwangDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        spider.logger.info('%s 准备下载' % request.url)

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        spider.logger.info('%s 下载完成，准备解析' % request.url)

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
