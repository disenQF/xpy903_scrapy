#!/usr/bin/python3
# coding: utf-8
from scrapy import cmdline


if __name__ == '__main__':
    cmdline.execute(['scrapy', 'crawl', 'hua', '-o', 'hua.json'])