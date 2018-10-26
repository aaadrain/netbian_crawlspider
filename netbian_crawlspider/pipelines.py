# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from . items import NetbianTitleItem
# from . items import NetbianTitleItem,NetbianImageItem,NetbianImageBodyItem

class NetbianImageDownloadPipeline(object):
	def __init__(self):
		self.count = 1


	def process_item(self,item,spider):

		imageName = item["imageName"]
		imageContent = item["imageContent"]
		imagePath = item['imagePath']
		print("[INFO]:正在准备下载<{}>".format(imageName))

		with open("./"+imagePath+'/'+imageName + '.jpg','wb') as f:
			f.write(imageContent)
			print("[INFO]:<{}>下载第{}张完成.".format(imageName,self.count))
			self.count += 1
		return item
