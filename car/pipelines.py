# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from twisted.enterprise import adbapi
from car.dataHandle.carBrand import carBrand
from car.dataHandle.carModel import carModel
from car.dataHandle.carVersion import carVersion


class CarPipeline:
    def __init__(self, conn):
        self.conn = conn

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        conn = pymysql.connect(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        # dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(conn=conn)

    def process_item(self, item, spider):
        # 品牌表数据
        if item['table_name'] == 'car_brand':
            carBrand().init(conn=self.conn, item=item)
        # 车系数据
        if item['table_name'] == 'car_model':
            carModel().init(conn=self.conn, item=item)
        # 车型数据
        if item['table_name'] == 'car_version':
            carVersion().init(conn=self.conn, item=item)
        return item

    def handle_error(self, failure):
        # 打印错误信息
        if failure:
            print(failure)
