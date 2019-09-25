# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from xiaohuar import ua


class XiaohuarPipeline(object):
    def process_item(self, item, spider):
        return item


class XiaohuaImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 发起图片下载的请求
        # 向 file_path()函数中传值（图片的作者名： 图片存放的目录名）
        return [Request(url,priority=500, meta={'name': item['name']})
                for url in item['image_urls']]

    def file_path(self, request, response=None, info=None):
        # 针对request请求，下载完成后准备写入文件时
        dir_name = request.meta['name']
        filename = hashlib.md5(request.url.encode('utf-8')).hexdigest()

        return '%s/%s.jpg' % (dir_name, filename)  # 返回图片文件的位置

    def item_completed(self, results, item, info):
        print('-----下载完成----')
        print(results)

        item[self.images_result_field] = [x['path'] for ok, x in results if ok]
        return item
