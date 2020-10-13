# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarBrandItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = scrapy.Field()
    id = scrapy.Field()
    first_letter = scrapy.Field()
    name = scrapy.Field()
    logo_url = scrapy.Field()


class CarBrandModelItem(scrapy.Item):
    table_name = scrapy.Field()
    id = scrapy.Field()
    sub_brand_name = scrapy.Field()
    brand_id = scrapy.Field()
    guid_price = scrapy.Field()
    car_price = scrapy.Field()
    car_type = scrapy.Field()
    name = scrapy.Field()
    cover_img = scrapy.Field()


class CarBrandModelVersionItem(scrapy.Item):
    spider_url = scrapy.Field()  # 爬取地址
    table_name = scrapy.Field()  # 表名
    id = scrapy.Field()

    name = scrapy.Field()  # 品牌型号版本名称
    category_type_id = scrapy.Field()  # 汽车类别id(car_categories表id)
    brand_id = scrapy.Field()  # 品牌id(car_brands表id)
    brand_model_id = scrapy.Field()  # 品牌型号id(car_brand_models表id)
    energy_type_id = scrapy.Field()  # 动力类型id
    engine_type_id = scrapy.Field()  # 发动机类型id
    gearbox_type_id = scrapy.Field()  # 变速箱类型id
    drive_way_type_id = scrapy.Field()  # 驱动方式类型id

    official_price = scrapy.Field()  # 官方指导售价
    xb_perk_price = scrapy.Field()  # 销巴补贴售价
    return_points_price = scrapy.Field()  # 积分全返价
    classify = scrapy.Field()  # 分类(排量、进气形式、马力)

    style_year = scrapy.Field()  # 款式年份
    displacements = scrapy.Field()  # 排量
    standard_type_id = scrapy.Field()  # 排放标准类型id
    horsepower = scrapy.Field()  # 马力
    images = scrapy.Field()  # 图片
    param_config = scrapy.Field()  # 参数配置
