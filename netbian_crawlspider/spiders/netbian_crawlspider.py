
# coding:utf-8
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider,Rule
from .. items import NetbianTitleItem

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  
"""
	crawlspider版本
"""
class NetBiAnCrawlspider(CrawlSpider):
	name = "netbian_crawlspider"
	allowed_domains = ['pic.netbian.com']
	base_url = 'http://pic.netbian.com'

	# 第一个是首页的请求,返回的默认响应交给所有的 Rule, 提取链接并发送请求
	start_urls = [base_url]    # start_urls  写错了不会报错.  但是程序白跑

	rules = [
		# 提取第一层链接,取得各个标题的链接
		Rule(LinkExtractor(allow=(r"\/4k"),deny=(r'html'))),
		Rule(LinkExtractor(allow=("4k[\w\/_]+\.html")),follow=True),
		Rule(LinkExtractor(allow=(r"tupian/\d+")),callback="parse_page",follow=True)
	]

	def parse_page(self,response):
		print("[INFO]:取得图片列表的链接集<{}>".format(response.url))
		# 取得图片的链接集
		image_link_list = response.xpath('//div[@class="photo-pic"]//img')
		next_link = response.xpath("//div[@class='page']/a").extract()

		for img in image_link_list:
			item = NetbianTitleItem()
			# 获取图片名字
			item["imageName"] = img.xpath("./@title").extract_first()
			item['imageUrls'] = img.xpath("./@src").extract_first()

			yield scrapy.Request(self.base_url + item['imageUrls'],meta={"imageName":item["imageName"]},callback=self.parse_image)
		

	def parse_image(self,response):
		print("[INFO]:图片详情的链接<{}>".format(response.url))

		item = NetbianTitleItem()
		imageName = response.meta["imageName"]
		imageContent = response.body
		item["imageName"] = imageName
		item["imageContent"] = imageContent
		item["imagePath"] = response.xpath('//div[@class="loaction"]//a[2]/text()').extract()
		yield item



"""
Cookie: __cfduid=d0c67d12951aeef59bffd10fd83a329f01537094949; yjs_id=c456daeb3e0bf5737e522f4e961640a9; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1537094950,1539184533,1539311932; Hm_lpvt_14b14198b6e26157b7eba06b390ab763=1539313586; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1539155947,1539184226,1539245912,1539313660; zkhanecookieclassrecord=%2C53%2C66%2C62%2C63%2C60%2C54%2C; zkhanlastsearchtime=1539330069; ctrl_time=1; PHPSESSID=f1b6946bd3be7c9da316cbc1a43ea680; 
driver.add_cookie({"name":"zkhanmlusername" , "value":"qq123996153709" })
driver.add_cookie({"name":"zkhanmluserid" , "value":"624388" })
driver.add_cookie({"name":"zkhanmlgroupid" , "value":"3" })
driver.add_cookie({"name":"zkhanmlrnd" , "value":"hNAWtgzj04t59bkssyOf" })
driver.add_cookie({"name":"zkhanmlauth" , "value":"8dea5ddf3fb9bcf062e94e03fbafd882" })
driver.add_cookie({"name":"Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e" , "value":"15393426"13})
"""









