# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from twisted.enterprise import adbapi


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
        cursor = self.conn.cursor()
        # 品牌表数据
        if item['table_name'] == 'car_brand':
            self.car_brand(cursor=cursor, item=item)
        # 车系数据
        if item['table_name'] == 'car_model':
            self.car_model(cursor=cursor, item=item)
        # 图片数据
        if item['table_name'] == 'car_version':
            self.car_version(cursor=cursor, item=item)
        return item

    def car_brand(self, cursor, item):
        cursor.execute("""SELECT id FROM car_brand WHERE `name` = '%s'""" % (item['name']))
        id = cursor.fetchone()
        if id is None:
            insert_sql = """insert into car_brand(`first_letter`,`name`,`logo_url`) VALUES(%s,%s,%s) """
            cursor.execute(insert_sql, (item['first_letter'], item['name'], item['logo_url']))
            item['id'] = cursor.lastrowid
            self.conn.commit()
        else:
            item['id'] = id['id']

    def car_model(self, cursor, item):
        cursor.execute("""SELECT id FROM car_model WHERE `name` = '%s'""" % (item['name']))
        id = cursor.fetchone()
        if id is None:
            insert_sql = """insert into car_model(`name`,`sub_brand_name`,`brand_id`,`cover_img`) VALUES(%s,%s,%s,%s)"""
            cursor.execute(insert_sql, (item['name'], item['sub_brand_name'], item['brand_id'], item['cover_img']))
            item['id'] = cursor.lastrowid
            self.conn.commit()
        else:
            item['id'] = id['id']

    def car_version(self, cursor, item):
        if 'images' in item:
            sql = """UPDATE car_version SET `images`=%s where id=%s"""
            cursor.execute(sql, (item['images'], item['id']))
        if 'config' in item:
            sql = """UPDATE car_version SET `config`=%s where id=%s"""
            cursor.execute(sql, (item['config'], item['id']))
        if 'name' in item:
            cursor.execute("""SELECT id FROM car_version WHERE `name` = '%s' and `model_id` = %s""" % (item['name'], item['model_id']))
            id = cursor.fetchone()
            if id is None:
                sql = """insert into car_version(`name`,`model_id`) VALUES(%s,%s)"""
                cursor.execute(sql, (item['name'], item['model_id']))
                item['id'] = cursor.lastrowid
            else:
                item['id'] = id['id']
            self.conn.commit()

    def handle_error(self, failure):
        # 打印错误信息
        if failure:
            print(failure)
