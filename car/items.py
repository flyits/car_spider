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
    brand_sub_name = scrapy.Field()
    brand_id = scrapy.Field()
    name = scrapy.Field()
    cover_img = scrapy.Field()


class CarBrandModelVersionItem(scrapy.Item):
    table_name = scrapy.Field()
    id = scrapy.Field()
    model_id = scrapy.Field()
    name = scrapy.Field()
    config = scrapy.Field()
    images = scrapy.Field()
