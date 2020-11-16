class carModel:
    conn = None

    def init(self, conn, item):
        self.conn = conn
        if  'id' in item and 'guid_price' in item:
            self.update(conn.cursor(), item)
        else:
            self.exists(conn.cursor(),item)

    def insert(self, cursor, item):
        insert_sql = """insert into car_model(`name`,`sub_brand_name`,`brand_id`,`cover_img`) VALUES(%s,%s,%s,%s)"""
        cursor.execute(insert_sql, (item['name'], item['sub_brand_name'], item['brand_id'], item['cover_img']))
        item['id'] = cursor.lastrowid
        self.conn.commit()

    def update(self,cursor,item):
        sql = """UPDATE car_model SET `guid_price`=%s,`car_price`=%s,`car_type`=%s where id=%s"""
        cursor.execute(sql, (item['guid_price'], item['car_price'], item['car_type'], item['id']))
        self.conn.commit()

    def exists(self, cursor, item):
        cursor.execute(
            """SELECT id FROM car_model WHERE `name` = '%s' and `brand_id` = %s""" % (item['name'], item['brand_id']))
        id = cursor.fetchone()
        if id is None:
            self.insert(cursor, item)
        else:
            item['id'] = id['id']
