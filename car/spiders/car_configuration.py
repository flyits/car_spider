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
img_base_url = 'http://photo.m.yiche.com/car/'
brandList = [
    '奥迪', '阿尔法·罗密欧', '阿斯顿·马丁', '爱驰', 'ALPINA', 'ARCFOX', 'ABT', 'AC Schnitzer', 'APEX', '奔驰', '宝马', '本田', '别克', '宝骏',
    '标致', '比亚迪', '奔腾', '保时捷', 'BEIJING汽车', '北汽新能源', '北汽威旺', '北汽幻速', '北汽昌河', '北汽制造', '铂驰', '宾利', '布加迪', '巴博斯', '长安汽车',
    '长安欧尚', '长安凯程', '车驰汽车', 'Cupra', 'Czinger', '长安跨越', '长城', '成功汽车', '大众', '东风风行', '东风风神', '东风风度', '东风小康', '东风风光',
    '东风', '东风·瑞泰特', '东南', '道奇', 'DS', '丰田', '福特', '菲亚特', '福迪', '法拉利', '福田', '广汽传祺', '广汽吉奥', '观致', '国能汽车', '国机智骏',
    'GFG Style', '海马', '红旗', '华泰', '哈弗', '汉腾', '哈飞', '华普', '汇众', '黄海', '恒天', '华颂', '华凯', '华骐', '恒驰', 'Icona', '吉利',
    '江淮', 'Jeep', '捷豹', '捷途', '江铃', '金杯', '金龙', '九龙', '金旅', '君马', '奇点汽车', '钧天汽车', '捷尼赛思', '江铃旅居车', '凯迪拉克', '克莱斯勒', '凯翼',
    '科尼赛克', '开瑞', 'KTM', '卡威', '陆风', '雷克萨斯', '林肯', '路虎', '雷诺', '领克', '铃木', '力帆', '劳斯莱斯', '路特斯', '兰博基尼', '猎豹', '理念',
    'Lorinser', '零跑汽车', '领途汽车', '罗夫哈特', '凌宝汽车', '雷丁', '马自达', '名爵', '玛莎拉蒂', '迈凯伦', '迈莎锐', 'Mahindra', '摩根', '纳智捷',
    '哪吒汽车', '讴歌', '欧拉', '欧宝', '帕加尼', 'Polestar极星', '佩奇奥', '奇瑞', '起亚', '启辰', '庆铃汽车', '前途', '骐铃汽车', '日产', '荣威', '瑞麒',
    'Rimac', '斯柯达', '斯巴鲁', 'SWM斯威汽车', '思皓', '三菱', '双环', '双龙', '上汽大通MAXUS', 'SRM鑫源', 'SSC', '思铭', '特斯拉', 'Troller',
    'VANTAS', 'Vega Innovations', '五菱汽车', '沃尔沃', 'WEY', '五十铃', '威兹曼', '潍柴汽车', '瓦滋', '雪铁龙', '雪佛兰', '现代', '英菲尼迪', '依维柯',
    '一汽', '野马汽车', '宇通客车', '云度', '云雀汽车', '远程汽车', '一汽解放', '众泰', '中华', '中兴', '中国重汽', ]


class CarConfiguration(scrapy.Spider):
    name = 'car_config'

    def start_requests(self):
        print('car_config running...')

        urls = ['http://car.m.yiche.com/']
        # 调试配置抓取，需设置callback为对应处理方法
        # urls = ['http://car.m.yiche.com/aodiq2haiwai/m139467/peizhi/?version_id=0']
        # 调试配置抓取，需设置callback为对应处理方法
        # urls = ['http://car.m.yiche.com/audi/?brand_id=1']
        # 调试图片抓取，需设置callback为对应处理方法
        # urls = ['http://photo.m.yiche.com/car/120422/']
        # urls = [            'http://car.m.yiche.com/kaiyunzhaiti/m142389/peizhi?table_name=car_version&brand_id=124&brand_model_id=2137&name=2020%E6%AC%BE+%E5%B0%8F%E5%8D%A1+2.8T+%E6%89%8B%E5%8A%A8+3.7%E7%B1%B3%E5%8D%95%E6%8E%92%E6%A0%8F%E6%9D%BF%E8%BD%BB%E5%8D%A1JX1041TCA25&classify=2.8T%2F85kW+%E6%B6%A1%E8%BD%AE%E5%A2%9E%E5%8E%8B&style_year=2020']
        # 调试图片抓取，需设置callback为对应处理方法
        # urls = ['http://car.m.yiche.com/x4/']
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
                if brand_item['name'] in brandList:
                    yield brand_item
                    count += 1
                    print(brand_item)
                    if url and self.black_list(url):
                        url = base_url + url + '?brand_id=' + str(brand_item['id'])
                        yield scrapy.Request(url=url.replace('/?', '?'), callback=self.model)
        # print(count)

    def model(self, response):
        brand_id = parse.parse_qs(parse.urlparse(response.url).query)['brand_id'][0]
        model_item = CarBrandModelItem()
        # 获取车系列表
        for model_list in response.xpath("//div[@class='brand-list']/div[@class='brand-item']"):
            model_item['table_name'] = 'car_model'
            model_item['brand_id'] = brand_id
            model_item['sub_brand_name'] = model_list.xpath(".//div[@class='brand-name']/text()").extract_first()
            for car_list in model_list.xpath(".//div[@class='brand-car']/a"):
                model_item['name'] = car_list.xpath(".//div[@class='car-name']/text()").extract_first().strip()
                model_item['cover_img'] = car_list.xpath(".//img/@data-original").extract_first().replace('_4.', '_8.')
                url = car_list.xpath("./@href").extract_first()
                yield model_item
                print(model_item)
                # print(model_item['name'])

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
        print(model_item)
        yield model_item
        # 获取车型版本列表
        version_item = CarBrandModelVersionItem()
        classify = ''
        for version_list in response.xpath("//div[@class='car-year-style-list']/div"):
            className = version_list.xpath("./@class").extract_first()

            if className.find('car-style-info') != -1:
                classify = version_list.xpath("./span[@class='c-style-val']/text()").extract_first()

            if className.find('c-style-warp') != -1:
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
                version_item['param_config'] = '{}'
                version_item['images'] = '{}'

                version_item['table_name'] = 'car_version'
                version_item['brand_id'] = brand_id
                version_item['brand_model_id'] = brand_model_id
                version_item['name'] = version_list.xpath('.//h1/text()').extract_first().strip()
                url = version_list.xpath(".//a/@href").extract_first() + 'peizhi'

                version_item['classify'] = classify
                version_item['style_year'] = version_list.xpath(
                    ".//div[@class='compare-box']/@data-year").extract_first()
                version_item['spider_url'] = base_url + url
                yield version_item
                print(version_item)
                # if url and self.black_list(url):
                #     url = base_url + url + '?' + parse.urlencode(version_item)
                #     yield scrapy.Request(url=url.replace('/?', '?'),
                #                          callback=self.config)

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

        configUrl = response.url
        carId = configUrl[configUrl.rfind('/m') + 2: configUrl.find('/peizhi')]
        images_url = img_base_url + str(carId)
        print(images_url)
        yield version_item
        print(version_item)
        if images_url:
            yield scrapy.Request(url=images_url, callback=self.images,
                                 cb_kwargs={'version_id': version_item['id']})
        #
        # print(config_item)

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

    # 黑名单url
    def black_list(self, url):
        black_url_list = [
            '/sikedavisionin/'
        ]
        if url in black_url_list:
            return False
        return True
