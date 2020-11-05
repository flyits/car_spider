import json

import scrapy
import pymysql
from car.items import CarBrandModelVersionItem


class CarImages(scrapy.Spider):
    name = 'car_images'

    def start_requests(self):

        urls = self.getUrlList()
        # urls = ['http://car.m.yiche.com/lifan620/m102576/peizhi?id=1145', ]
        # 'http://car.m.yiche.com/v8vantage/m116823/peizhi?table_name=car_version&brand_id=3&brand_model_id=3&name=2016%E6%AC%BE+4.7L+Coupe&classify=4.7L%2F313kW+%E8%87%AA%E7%84%B6%E5%90%B8%E6%B0%94&style_year=2016']
        for url in urls:
            carId = url['url'][url['url'].rfind('/m') + 2: url['url'].find('/peizhi')]
            images_url = 'http://photo.m.yiche.com/car/' + str(carId)
            yield scrapy.Request(url=images_url, callback=self.images,
                                 cb_kwargs={'version_id': url['id']})

    def images(self, response, version_id):
        images = []
        for title in response.xpath("//div[@class='tt-first tt-first-no-bd']"):
            if title.xpath('.//h3/text()').extract_first() == '官方':
                more_images = title.xpath('.//a/@href').extract_first()
                # 是否有更多图片，否则直接爬取当前页面上的官方图片
                if more_images:
                    url = 'http://photo.m.yiche.com' + more_images
                    yield scrapy.Request(url=url, dont_filter=True, callback=self.more_images,
                                         cb_kwargs={'version_id': version_id})
                else:
                    for image in response.xpath("//div[@class='pic-select-car'][last()]//ul//li"):
                        images.append(image.xpath('.//img/@src').extract_first())
                    yield self.insert_images(images, version_id)

    def more_images(self, response, version_id):
        images = []
        for image in response.xpath("//ul[@class='ul-list']//li"):
            image_url = image.xpath('.//img/@src').extract_first().replace('_4.', '_8.')
            images.append(image_url)
        yield self.insert_images(images, version_id)

    def insert_images(self, images, version_id):
        if images:
            print(images)
            version_item = CarBrandModelVersionItem()
            version_item['table_name'] = 'car_version'
            version_item['id'] = version_id
            version_item['images'] = json.dumps(images)
            # print(version_item)
            return version_item
    def getUrlList(self):
        db = pymysql.connect("172.29.0.217", "root", "root", "car_spider")

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT spider_url,id FROM `car_version` WHERE images = '{}'  ")

        # 使用 fetchone() 方法获取全部数据.
        data = cursor.fetchall()
        urls = []
        for url in data:
            id = url[1]
            url = url[0][:url[0].find('?')] + '?id=' + str(id)

            urls.append({"id":id,"url":url})
        # 关闭数据库连接
        db.close()
        return urls
