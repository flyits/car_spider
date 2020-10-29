import json
from urllib import parse

import scrapy
from scrapy_selenium import SeleniumRequest
import pymysql
from car.types import Types
from car.items import CarBrandModelVersionItem


class CarSpider(scrapy.Spider):
    name = 'car_spider'

    def start_requests(self):

        urls = self.getUrlList()
        # urls = ['http://car.m.yiche.com/hafum4/m115390/peizhi?id=52496', ]
        # 'http://car.m.yiche.com/v8vantage/m116823/peizhi?table_name=car_version&brand_id=3&brand_model_id=3&name=2016%E6%AC%BE+4.7L+Coupe&classify=4.7L%2F313kW+%E8%87%AA%E7%84%B6%E5%90%B8%E6%B0%94&style_year=2016']
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        version_item = CarBrandModelVersionItem()
        # 参数初始化
        version_item['category_type_id'] = 0
        version_item['energy_type_id'] = 0
        version_item['engine_type_id'] = 0
        version_item['gearbox_type_id'] = 0
        version_item['drive_way_type_id'] = 0
        version_item['official_price'] = 0
        version_item['xb_perk_price'] = 0
        version_item['return_points_price'] = 0
        version_item['displacements'] = ''
        version_item['standard_type_id'] = 0
        version_item['horsepower'] = ''
        version_item['param_config'] = ''
        version_item['table_name'] = 'car_version'
        version_item['id'] = parse.parse_qs(parse.urlparse(response.url).query)['id'][0]

        config = []
        configName = response.xpath("//div[@id='content-iscoll']/div/div/@data-flag").extract_first()
        config = self.subConfig(configName, response.xpath("//div[@id='content-iscoll']/div/div/*"), config,
                                version_item)
        version_item['param_config'] = json.dumps(config, ensure_ascii=False)

        print(response.url)
        print(version_item)
        # yield version_item

    def subConfig(self, configName, configList, config, version_item):
        sub_config = {'name': configName, 'sub_config': []}
        for value in configList:
            tableId = value.xpath("./@id").extract_first()
            configName = value.xpath("./@data-flag").extract_first()
            if tableId:
                for subConfig in value.xpath('.//tr'):
                    subConfigName = subConfig.xpath("./@data-name").extract_first().strip()
                    # 若值为颜色列表
                    if subConfig.xpath("./td/@class").extract_first().find("color-box") != -1:
                        subConfigValue = []
                        for item in subConfig.xpath(".//i"):
                            color = item.xpath("./@style").extract_first()
                            start = color.rfind("background-color:") + 17
                            subConfigValue.append(color[start:start + 7])
                    else:
                        subConfigValue = subConfig.xpath(".//span/text()").extract_first().strip()
                    sub_config['sub_config'].append({"name": subConfigName, "value": subConfigValue})
                    Types().getTypeId(version_item, subConfigName, subConfigValue)
                config.append(sub_config)
            if configName:
                # 易车改版后dom结构非并列，而是层级递进，需递归遍历抓取子配置
                self.subConfig(configName, value.xpath('./*'), config, version_item)
        return config

    def getUrlList(self):
        db = pymysql.connect("car_mysql", "root", "root", "car_spider")

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT spider_url,id FROM `car_version` WHERE param_config = '' or param_config = '[]'")

        # 使用 fetchone() 方法获取全部数据.
        data = cursor.fetchall()
        urls = []
        for url in data:
            id = url[1]
            url = url[0][:url[0].find('?')] + '?id=' + str(id)

            urls.append(url)
        # 关闭数据库连接
        db.close()
        return urls
