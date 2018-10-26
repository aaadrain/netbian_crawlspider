# coding:utf-8
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from ..items import NetbianTitleItem

from scrapy_redis.spiders import RedisCrawlSpider

import sys

reload(sys)
sys.setdefaultencoding('utf8')
"""
	redis-crawlspider版本
"""


class NetBiAnredisCrawlspider(RedisCrawlSpider):
    name = "netbian_rediscrawlspider"
    allowed_domains = ['pic.netbian.com']
    base_url = 'http://pic.netbian.com'

    # 第一个是首页的请求,返回的默认响应交给所有的 Rule, 提取链接并发送请求
    # start_urls = [base_url]    # start_urls  写错了不会报错.  但是程序白跑
    redis_key = "netbianrediscrawlspider:start_urls"
    rules = [
        # 提取第一层链接,取得各个标题的链接
        Rule(LinkExtractor(allow=(r"\/4k"), deny=(r'html'))),
        Rule(LinkExtractor(allow=("4k[\w\/_]+\.html")), follow=True),
        Rule(LinkExtractor(allow=(r"tupian/\d+")), callback="parse_page", follow=True)
    ]

    def parse_page(self, response):
        print("[INFO]:取得图片列表的链接集<{}>".format(response.url))
        # 取得图片的链接集
        image_link_list = response.xpath('//div[@class="photo-pic"]//img')
        next_link = response.xpath("//div[@class='page']/a").extract()

        for img in image_link_list:
            item = NetbianTitleItem()
            # 获取图片名字
            item["imageName"] = img.xpath("./@title").extract_first()
            item['imageUrls'] = img.xpath("./@src").extract_first()

            yield scrapy.Request(self.base_url + item['imageUrls'], meta={"imageName": item["imageName"]},
                                 callback=self.parse_image)

    def parse_image(self, response):
        print("[INFO]:图片详情的链接<{}>".format(response.url))

        item = NetbianTitleItem()
        imageName = response.meta["imageName"]
        imageContent = response.body
        item["imageName"] = imageName
        item["imageContent"] = imageContent
        item["imagePath"] = response.xpath('//div[@class="loaction"]//a[2]/text()').extract()
        yield item
