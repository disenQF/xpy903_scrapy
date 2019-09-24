# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

import selenium
import time
from scrapy import signals, Request
from scrapy.http import HtmlResponse
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from qcc import ua, cookies


class QccSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
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


class QccDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # 设置请求头
        # scrapy.Request
        # request.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        request.headers['User-Agent'] = ua.get()

        request.headers['Sec-Fetch-Mode'] = 'cors'
        request.headers['Sec-Fetch-Site'] = 'none'
        request.headers['Sec-Fetch-User'] = '?1'
        request.headers['Upgrade-Insecure-Requests'] = 1

        # 注： cookies是dict类型
        request.cookies = cookies.get()

        # 设置请求的代理 request.meta['proxy'] = 'http://ip:port'

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

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


class SeleniumMiddleware(object):
    def __init__(self):
        options = Options()
        # options.add_argument('--headless')  # 无头浏览器，不显示窗口
        # options.add_argument('--disable-gpu')

        # 可执行驱动程序的位置
        driver_path = '/Users/apple/PycharmProjects/scrapy_spider/driver/chromedriver'

        self.chrome = Chrome(options=options,
                             executable_path=driver_path)

        self.is_logined = False  # 默认未登录

    def get_track(self, distance):
        track = []
        current = 0
        mid = distance * 3 / 4
        t = 0.2
        v = 0
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track

    def process_request(self, request, spider):
        if not self.is_logined:
            # 打开登录页面，实现登录
            self.chrome.get('https://www.qichacha.com/user_login')
            ui.WebDriverWait(self.chrome, 30).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'login-panel'))
            )

            self.chrome.find_element_by_css_selector('.login-panel-head div:nth-child(2) a').click()
            self.chrome.find_element_by_id('nameNormal').send_keys('17791692095')
            self.chrome.find_element_by_id('pwdNormal').send_keys('disen666')

            # 处理滑动问题
            slide_span = self.chrome.find_element_by_css_selector('#dom_id_one span')
            slide_div = self.chrome.find_element_by_css_selector('#dom_id_one')

            actions = ActionChains(self.chrome)
            actions.click_and_hold(slide_span).perform()
            actions.reset_actions()

            print(slide_div.rect)
            width = slide_div.rect['width'] # 348
            offset = round(width/10, 2)
            for cnt in range(1, 11):  # 1,...10
                actions.move_by_offset(offset*cnt, 0).perform()
                time.sleep(0.1)

            actions.reset_actions()

            self.chrome.find_element_by_css_selector('.login-btn').click()

            self.is_logined = True

        time.sleep(3)

        self.chrome.get(request.url)

        if request.url.find('/firm_') == -1:
            ui.WebDriverWait(self.chrome, 30).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'pills-after'))
            )
        else:
            ui.WebDriverWait(self.chrome, 30).until(
                EC.visibility_of_all_elements_located((By.ID, 'Cominfo'))
            )

        html = self.chrome.page_source  # str

        return HtmlResponse(request.url,
                            body=html.encode('utf-8'),
                            request=request)
