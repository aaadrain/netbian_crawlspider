# coding:utf-8
import time
from selenium import webdriver
import scrapy
from retrying import retry
class SeleniumMinddlewre(object):
    def __init__(self):
        # self.driver = webdriver.Chrome()    # 有界面
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--proxy-server=http://106.75.164.15:3128")
        self.driver = webdriver.Chrome(chrome_options=self.options)
        

        # 无界面
        # self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless")
        # self.driver = webdriver.Chrome(chrome_options = self.options)


        self.flag = True
        self.load_ok_count = 0

    @retry(stop_max_attempt_number=20,wait_fixed=200)
    def retry_load_image(self,request,spider):
        try:
            self.driver.find_element_by_class_name("downpic").click()
            time.sleep(3)
            self.load_ok_count += 1
            print("[INFO] {} Image <{}> is loadding!".format(self.load_ok_count,request.url))

        except:
            spider.logger.info("[Retry load image [{}] times]<{}>".format(self.retry_count,request.url))

            self.retry_count = 1 
            raise Exception("[INFO]<{}> image load failed".format(request.url)) 



    def process_request(self,request,spider):

        if "tupian" in request.url:
            self.retry_count = 1 

            # 打开下载页面
            self.driver.get(request.url)
            # time.sleep(5)
            if self.flag:
                self.driver.add_cookie({"name":"__cfduid" , "value":"d0c67d12951aeef59bffd10fd83a329f01537094949"})
                self.driver.add_cookie({"name":"yjs_id" , "value":"c456daeb3e0bf5737e522f4e961640a9"})
                self.driver.add_cookie({"name":"Hm_lvt_14b14198b6e26157b7eba06b390ab763" , "value":"1537094950,1539184533,1539311932"})
                self.driver.add_cookie({"name":"zkhanlastsearchtime" , "value":"1539330069"})
                self.driver.add_cookie({"name":"ctrl_time" , "value":"1"})
                self.driver.add_cookie({"name":"Hm_lvt_526caf4e20c21f06a4e9209712d6a20e" , "value":"1539184226,1539245912,1539313660,1539360772"})
                self.driver.add_cookie({"name":"PHPSESSID" , "value":"40fac39568647438a42f8ed20426aa52"})
                self.driver.add_cookie({"name":"Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e" , "value":"1539360792"})
                self.driver.add_cookie({"name":"zkhanmlusername" , "value":"qq123996153709" })
                self.driver.add_cookie({"name":"zkhanmluserid" , "value":"624388" })
                self.driver.add_cookie({"name":"zkhanmlgroupid" , "value":"3" })
                self.driver.add_cookie({"name":"zkhanmlrnd" , "value":"z2NJqVpxeYvQIUxt3LvS" })
                self.driver.add_cookie({"name":"zkhanmlauth" , "value":"8caaca502d4c41731b196ce820a2932d" })

                self.flag = False

            if not int(self.load_ok_count) % 100:
                self.flag = True


            self.driver.refresh()
            try:
                # time.sleep(2)
                self.retry_load_image(request,spider)
                # self.driver.find_element_by_class_name("downpic").click()
                # time.sleep(3)

                html = self.driver.page_source

                response = scrapy.http.HtmlResponse(
                    url=self.driver.current_url,
                    body=html.encode("utf-8"),
                    encoding='utf-8',
                    request=request
                )
                return response
            except Exception as e:
                spider.logger.info(e)
                return request

"""
self.driver.add_cookie({"name":"__cfduid" , "value":"d0c67d12951aeef59bffd10fd83a329f01537094949"})
self.driver.add_cookie({"name":"yjs_id" , "value":"c456daeb3e0bf5737e522f4e961640a9"})
self.driver.add_cookie({"name":"Hm_lvt_14b14198b6e26157b7eba06b390ab763" , "value":"1537094950,1539184533,1539311932"})
self.driver.add_cookie({"name":"zkhanlastsearchtime" , "value":"1539330069"})
self.driver.add_cookie({"name":"ctrl_time" , "value":"1"})
self.driver.add_cookie({"name":"Hm_lvt_526caf4e20c21f06a4e9209712d6a20e" , "value":"1539184226,1539245912,1539313660,1539360772"})
self.driver.add_cookie({"name":"PHPSESSID" , "value":"40fac39568647438a42f8ed20426aa52"})
self.driver.add_cookie({"name":"Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e" , "value":"1539360792"})
self.driver.add_cookie({"name":"zkhanmlusername" , "value":"qq123996153709" })
self.driver.add_cookie({"name":"zkhanmluserid" , "value":"624388" })
self.driver.add_cookie({"name":"zkhanmlgroupid" , "value":"3" })
self.driver.add_cookie({"name":"zkhanmlrnd" , "value":"z2NJqVpxeYvQIUxt3LvS" })
self.driver.add_cookie({"name":"zkhanmlauth" , "value":"8caaca502d4c41731b196ce820a2932d" })

"""
"""
__cfduid=d0c67d12951aeef59bffd10fd83a329f01537094949; 
yjs_id=c456daeb3e0bf5737e522f4e961640a9; 
Hm_lvt_14b14198b6e26157b7eba06b390ab763=1537094950,1539184533,1539311932; 
zkhanlastsearchtime=1539330069; 
ctrl_time=1; 
Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1539184226,1539245912,1539313660,1539360772; 
PHPSESSID=40fac39568647438a42f8ed20426aa52;
zkhanmlusername=qq123996153709; 
zkhanmluserid=624388; 
zkhanmlgroupid=3; 
zkhanmlrnd=z2NJqVpxeYvQIUxt3LvS; 
zkhanmlauth=8caaca502d4c41731b196ce820a2932d; 
Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1539360792
"""
            