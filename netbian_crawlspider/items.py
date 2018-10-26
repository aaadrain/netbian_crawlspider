# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NetbianTitleItem(scrapy.Item):
	# define the fields for your item here like:
	# 类别名
	title_name = scrapy.Field()
	# 类别链接
	title_links = scrapy.Field()

# class NetbianImageItem(scrapy.Item):
	# 图片链接
	imageUrls = scrapy.Field()
	# 图片保存路径
	imagePath = scrapy.Field()
	# 图片名字
	imageName = scrapy.Field()

# class NetbianImageBodyItem(scrapy.Item):
	# 图片内容
	imageContent = scrapy.Field()