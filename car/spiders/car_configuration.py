# _*_ coding: utf-8 _*_
import scrapy
import json
import random
from urllib import parse
from car.items import CarBrandItem
from car.items import CarBrandModelItem
from car.items import CarBrandModelVersionItem
from car.types import Types

base_url = 'http://car.m.yiche.com'
img_base_url = 'http://photo.m.yiche.com'


class CarConfiguration(scrapy.Spider):
    name = 'car_config'

    def start_requests(self):
        print('car_config running...')

        urls = ['http://car.m.yiche.com/']
        # 调试配置抓取，需设置callback为对应处理方法
        # urls = ['http://car.m.yiche.com/aodiq2haiwai/m139467/peizhi/?version_id=0']
        # 调试配置抓取，需设置callback为对应处理方法
        # urls = ['https://car.m.yiche.com/maxusv80/?brand_model_id=1&brand_id=1']
        # 调试图片抓取，需设置callback为对应处理方法
        # urls = ['http://photo.m.yiche.com/car/120422/']
        # 调试图片抓取，需设置callback为对应处理方法
        # urls = [
        #     'http://car.m.yiche.com/yufenga100/m129883/peizhi?table_name=car_version&brand_id=65&brand_model_id=352&name=2018%E6%AC%BE+A100+3.0T+%E6%89%8B%E5%8A%A8+%E8%BD%BD%E5%AE%A250M+ZD30+%E9%AB%98%E9%85%8D%E7%89%88+12%E5%BA%A7&classify=%E5%8F%82%E9%85%8D%E6%9C%AA%E5%85%AC%E5%B8%83&style_year=2020']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # 获取品牌列表
        brand_list = response.xpath("//div[@class='brand-content']//dl")
        brand_item = CarBrandItem()
        count = 0
        for brand in brand_list:
            # 获取品牌首字母
            brand_item['table_name'] = 'car_brand'
            brand_item['first_letter'] = brand.xpath(".//dt/text()").extract_first()
            # 获取该首字母下品牌列表
            sub_brand_list = brand.xpath(".//dd")
            for sub_brand in sub_brand_list:
                # 获取品牌名
                brand_item['name'] = sub_brand.xpath(".//p/text()").extract_first()
                # 获取logo地址
                brand_item['logo_url'] = sub_brand.xpath(".//img/@data-original").extract_first().replace('_4.', '_8.')
                # 获取该品牌 A标记 跳转地址（下级车型）
                url = sub_brand.xpath(".//a/@href").extract_first()
                # 返回品牌数据到 pipeline 写入数据库，返回携带新增id的item
                yield brand_item
                count += 1
                # print(brand_item)
                if url and self.black_list(url):
                    url = base_url + url + '?brand_id=' + str(brand_item['id'])
                    yield scrapy.Request(url=url.replace('/?', '?'), callback=self.model)
        # print(count)

    def model(self, response):
        brand_id = parse.parse_qs(parse.urlparse(response.url).query)['brand_id'][0]
        model_item = CarBrandModelItem()
        # 获取车系列表
        for model_list in response.xpath("//div[@class='brand-list']"):
            model_item['table_name'] = 'car_model'
            model_item['brand_id'] = brand_id
            model_item['sub_brand_name'] = model_list.xpath(".//div[@class='brand-name']/text()").extract_first()
            for car_list in model_list.xpath(".//div[@class='brand-car']"):
                model_item['name'] = car_list.xpath(".//div[@class='car-name']/text()").extract_first().strip()
                model_item['cover_img'] = car_list.xpath(".//img/@data-original").extract_first().replace('_4.', '_8.')
                url = car_list.xpath(".//a/@href").extract_first()
                yield model_item
                # print(model_item)

                if url and self.black_list(url):
                    url = base_url + url + '?brand_model_id=' + str(model_item['id']) + '&brand_id=' + str(brand_id)
                    yield scrapy.Request(url=url.replace('/?', '?'),
                                         callback=self.version)

    def version(self, response):
        brand_id = parse.parse_qs(parse.urlparse(response.url).query)['brand_id'][0]
        brand_model_id = parse.parse_qs(parse.urlparse(response.url).query)['brand_model_id'][0]
        model_item = CarBrandModelItem()
        car_price = response.xpath("//span[@class='car-price']/text()").extract_first()
        guid_price = response.xpath("//div[@class='guid-price']/em[1]/text()").extract_first()
        car_type = response.xpath("//div[@class='guid-price']/span[2]/text()").extract_first()
        if car_price != '暂无报价' and car_price != '暂无预售价' and car_price is not None:
            car_price = car_price + '万'
        if guid_price == '指导价' or guid_price == '预售价':
            guid_price = response.xpath("//div[@class='guid-price']/span[1]/text()").extract_first()
        if guid_price == '暂无预售价' or guid_price == '暂无指导价' or guid_price is None:
            car_type = response.xpath("//div[@class='guid-price']/span[1]/text()").extract_first()
        model_item['guid_price'] = guid_price
        model_item['car_price'] = car_price
        model_item['car_type'] = car_type
        model_item['table_name'] = 'car_model'
        model_item['id'] = brand_model_id
        # print(model_item)
        yield model_item
        # 获取车型版本列表
        version_item = CarBrandModelVersionItem()
        classify = ''
        for version_list in response.xpath("//div[@class='car-year-style-list']/div"):
            className = version_list.xpath("./@class").extract_first()

            if className.find('car-style-info') != -1:
                classify = version_list.xpath("./span[@class='c-style-val']/text()").extract_first()

            if className.find('c-style-warp') != -1:
                version_item['table_name'] = 'car_version'
                version_item['brand_id'] = brand_id
                version_item['brand_model_id'] = brand_model_id
                version_item['name'] = version_list.xpath('.//h1/text()').extract_first().strip()
                url = version_list.xpath(".//a/@href").extract_first() + 'peizhi'

                version_item['classify'] = classify
                version_item['style_year'] = version_list.xpath(
                    ".//div[@class='compare-box']/@data-year").extract_first()
                print(version_item)
                if url and self.black_list(url):
                    url = base_url + url + '?' + parse.urlencode(version_item)
                    # yield scrapy.Request(url=url.replace('/?', '?'),
                    #                      callback=self.config)

    def config(self, response):
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

        version_item['spider_url'] = response.url
        version_item['table_name'] = 'car_version'
        version_item['brand_id'] = parse.parse_qs(parse.urlparse(response.url).query)['brand_id'][0]
        version_item['brand_model_id'] = parse.parse_qs(parse.urlparse(response.url).query)['brand_model_id'][0]
        version_item['name'] = parse.parse_qs(parse.urlparse(response.url).query)['name'][0]
        version_item['classify'] = parse.parse_qs(parse.urlparse(response.url).query)['classify'][0]
        version_item['style_year'] = parse.parse_qs(parse.urlparse(response.url).query)['style_year'][0]
        config_item = []
        sub_config = {}

        configsLength = len(response.xpath("//tr"))
        for i, config in enumerate(response.xpath("//tr")):
            # 判断当前元素是否 子配置名 如：基本信息、车身尺寸等 或为
            if config.xpath('./@id').extract_first():
                # 判断当前子配置是否已经爬取完成，完成写入主配置
                if sub_config:
                    config_item.append(sub_config)
                # 初始化子配置
                sub_config = {'name': config.xpath('.//span/text()').extract_first(), 'sub_config': []}
            else:
                # 获取子配置下配置名
                name = config.xpath('.//th/text()').extract_first()
                value = []
                # 检测当前元素是否为车辆颜色信息
                if config.xpath('.//td[@class="m-car-color"]'):
                    for color in config.xpath(".//td[@class='m-car-color']//li"):
                        value.append(color.xpath(".//span/@style").extract_first()[-7:])
                else:
                    # 检测当前元素是否有多个配置值
                    if config.xpath('.//div[@class="l"]'):
                        for item in config.xpath('.//div[@class="l"]'):
                            value.append(
                                item.xpath('./i/text()').extract_first() + ' ' + item.xpath('./text()').extract_first())
                    if len(value) == 1:
                        value = value[0]
                    else:
                        value = config.xpath('.//td/text()').extract_first()
                # print(sub_config)
                #  写入子配置
                sub_config['sub_config'].append({
                    'name': name,
                    'value': value
                })
                Types().getTypeId(version_item, name, value)
            # 检测循环结束，写入主配置
            if i + 1 == configsLength and sub_config:
                config_item.append(sub_config)
        print(config_item)
        if config_item:
            version_item['param_config'] = json.dumps(config_item, ensure_ascii=False)
        yield version_item

        images_url = response.xpath('//*[@id="container"]/div[1]/div[3]/ul/li[4]/a/@href').extract_first()
        if images_url:
        yield scrapy.Request(url='http:' + images_url, callback=self.images,
                             cb_kwargs={'version_id': version_item['id']})

        # print(config_item)

    def images(self, response, version_id):
        images = []
        for title in response.xpath("//div[@class='tt-first tt-first-no-bd']"):
            if title.xpath('.//h3/text()').extract_first() == '官方':
                more_images = title.xpath('.//a/@href').extract_first()
                # 是否有更多图片，否则直接爬取当前页面上的官方图片
                if more_images:
                    yield scrapy.Request(url=img_base_url + more_images, dont_filter=True, callback=self.more_images,
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
            version_item = CarBrandModelVersionItem()
            version_item['table_name'] = 'car_version'
            version_item['id'] = version_id
            version_item['images'] = json.dumps(images)
            # print(version_item)
            return version_item

    # 黑名单url
    def black_list(self, url):
        black_url_list = [
            '/sikedavisionin/'
        ]
        if url in black_url_list:
            return False
        return True
