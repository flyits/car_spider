import scrapy
import chompjs
import js2xml
import urllib
import json
import pymysql
import random
import requests
import time
import hashlib
import lxml.etree
from js2xml.utils.vars import get_vars
from scrapy import Request


class CarSpider(scrapy.Spider):
    name = 'car_spider'

    def start_requests(self):
        db = pymysql.connect("car_mysql", "root", "root", "car_spider")

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT spider_url FROM `car_version` WHERE param_config = '' ")

        # 使用 fetchone() 方法获取全部数据.
        data = cursor.fetchall()
        urls = []
        for url in data:
            urls.append(url[0])
        self.header()
        # 关闭数据库连接
        db.close()
        # urls = ['http://car.m.yiche.com/fengguang330/m135672/peizhi?table_name=car_version&brand_id=58&brand_model_id=233&name=2019%E6%AC%BE+330S+1.5L+%E6%89%8B%E5%8A%A8+%E8%88%92%E9%80%82%E5%9E%8B+%E5%9B%BDVI&classify=1.5L%2F85kW+%E8%87%AA%E7%84%B6%E5%90%B8%E6%B0%94&style_year=2019',]
        #         'http://car.m.yiche.com/v8vantage/m116823/peizhi?table_name=car_version&brand_id=3&brand_model_id=3&name=2016%E6%AC%BE+4.7L+Coupe&classify=4.7L%2F313kW+%E8%87%AA%E7%84%B6%E5%90%B8%E6%B0%94&style_year=2016']
        # for url in urls:
        # yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):

        for i, x in enumerate(response.xpath('//script')):
            js = x.xpath('.//text()').extract_first()
            if js is not None and i == 20:
                carInfo = json.loads(get_vars(js2xml.parse(js))['carInfo'])

                param = json.dumps({'serialId': carInfo['serialId'], 'cityId': 201, 'carId': carInfo['carId']})
                url = "http://car.m.yiche.com/web_api/car_model_api/api/v1/car/config_new_param?cid=601&param=%s" % (
                    urllib.parse.quote(param))
                headers = {
                    "Connection": "keep-alive",
                    "dvid": "a3029536-d676-4906-a1e1-b71a1686116a",
                    "gudpar": "06d94200a2d753fca07b3a2c68e97cc8",
                    "x-platform": "phone",
                    "X-Tingyun-Id": "8gU8qeI8HW4;r=727441526",
                    "X-Requested-With": "XMLHttpRequest",
                    "uidl": "",
                    "x-sign": "06a9bcc1a6faccaf7860e4f2409f6e21",
                    "reqid": "f66c57348ebaea049177e4a7b652802c",
                    "x-city-id": "201",
                    "osl": "2",
                    "osvl": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 SocketLog(tabid=30&client_id=)",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "x-timestamp": str(round(time.time() * 1000)),
                    "x-ip-address": "113.251.61.183",
                    "x-user-guid": "a3029536-d676-4906-a1e1-b71a1686116a",
                    "gudslf": "a10d9a249eec3ca88ed1b0f7e061857e",
                    "ver": "v10.40.0",
                    "Referer": "http://car.m.yiche.com/aichiu5ion/m131941/peizhi?table_name=car_version&brand_id=4&brand_model_id=9&name=2019%E6%AC%BE+PRO%2B&classify=%E7%94%B5%E5%8A%A8%E8%BD%A6%2F140kW+%E7%BB%AD%E8%88%AA623km&style_year=2019",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": "selectcity=110100; selectcityid=201; selectcityName=%E5%8C%97%E4%BA%AC; report-cookie-id=829474087_1602725595135; auto_id=aa18e47515e74603a1d2fd943541a4c5; locatecity=500100; CIGDCID=20bce3d0220f47e3b0b78cb1ddec9957; G_CIGDCID=20bce3d0220f47e3b0b78cb1ddec9957; Hm_lvt_03efd23dfd835817ac8b9504cf0e715d=1602725597; UserGuid=a3029536-d676-4906-a1e1-b71a1686116a; CIGUID=a3029536-d676-4906-a1e1-b71a1686116a; bitauto_ipregion=113.251.61.183%3a%e9%87%8d%e5%ba%86%e5%b8%82%3b201%2c%e5%8c%97%e4%ba%ac%2cbeijing; Hm_lpvt_03efd23dfd835817ac8b9504cf0e715d=1602725657",
                }
                # respose = requests.get(url=url, headers=headers)
                # print(json.loads(respose.content))

            # data = chompjs.parse_js_object(js)
            # print(data)

    # javascript = response.css('script::text').get()
    # print(javascript)
    # csId  = chompjs.parse_js_object(javascript)
    # print(csId )

    def sign(self, requestParam):
        l = 'DB2560A6EBC65F37A0484295CD4EDD25'
        Str = 'cid' + requestParam['cid'] + '&param=' + requestParam['param'] + l + str(round(time.time() * 1000))
        return hashlib.md5(Str)

    def header(self):
        Str = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
        print(Str)
        newStr = ''
        for i, s in enumerate(Str):
            randomNumber = random.randint(1, 16)
            if s == 'x':
                randomNumber = 3 & randomNumber | 8
            if s == '-':
                continue
            randomNumber = int(randomNumber,base=16)
            print(i, s,randomNumber)

            newStr = Str.replace(s, str(randomNumber),1)
        print(newStr)
