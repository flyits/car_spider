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
        # 车型数据
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

        if 'car_price' in item:
            sql = """UPDATE car_model SET `guid_price`=%s,`car_price`=%s,`car_type`=%s where id=%s"""
            cursor.execute(sql, (item['guid_price'], item['car_price'], item['car_type'], item['id']))
            self.conn.commit()
        if 'name' in item:
            cursor.execute(
                """SELECT id FROM car_model WHERE `name` = '%s' and `brand_id` = %s""" % (
                    item['name'], item['brand_id']))
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
            self.conn.commit()
        if 'param_config' in item:
            sql = """UPDATE car_version SET `param_config`=%s,`category_type_id`=%s,`energy_type_id`=%s, `engine_type_id`=%s,
             `gearbox_type_id`=%s,`drive_way_type_id`=%s,`official_price`=%s, `xb_perk_price`=%s,  `return_points_price`=%s, 
                  `displacements`=%s,`standard_type_id`=%s,  `horsepower`=%s
                 where id=%s"""
            cursor.execute(sql, (
                item['param_config'], item['category_type_id'], item['energy_type_id'], item['engine_type_id'],
                item['gearbox_type_id'], item['drive_way_type_id'], item['official_price'], item['xb_perk_price'],
                item['return_points_price'],
                item['displacements'], item['standard_type_id'], item['horsepower'], item['id']))
            self.conn.commit()
        # if 'classify' in item:
        #     sql = """UPDATE car_version SET `classify`=%s,`style_year`=%s where id=%s"""
        #     cursor.execute(sql, (item['classify'], item['style_year'], item['id']))
        if 'name' in item:
            cursor.execute("""SELECT id FROM car_version WHERE `name` = '%s' and `brand_model_id` = %s""" % (
                item['name'], item['brand_model_id']))
            id = cursor.fetchone()
            if id is None:
                sql = """insert into car_version(`name`,`brand_id`, `brand_model_id`, `classify`, `style_year`,
                `category_type_id`,`energy_type_id`, `engine_type_id`, `gearbox_type_id`,
                 `drive_way_type_id`,`official_price`, `xb_perk_price`,  `return_points_price`, 
                  `displacements`,`standard_type_id`,  `horsepower`,  `param_config`,`spider_url`
                ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                cursor.execute(sql, (
                    item['name'], item['brand_id'], item['brand_model_id'], item['classify'], item['style_year'],
                    item['category_type_id'], item['energy_type_id'], item['engine_type_id'],
                    item['gearbox_type_id'], item['drive_way_type_id'],
                    item['official_price'], item['xb_perk_price'], item['return_points_price'],
                    item['displacements'], item['standard_type_id'], item['horsepower'], item['param_config'],
                    item['spider_url']
                ))
                item['id'] = cursor.lastrowid
                self.conn.commit()
            else:
                item['id'] = id['id']

    def handle_error(self, failure):
        # 打印错误信息
        if failure:
            print(failure)
