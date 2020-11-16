class carBrand(object):
    conn = None

    def init(self, conn, item):
        self.conn = conn
        self.exists(conn.cursor(), item)

    def insert(self, cursor, item):
        insert_sql = """insert into car_brand(`first_letter`,`name`,`logo_url`) VALUES(%s,%s,%s) """
        cursor.execute(insert_sql, (item['first_letter'], item['name'], item['logo_url']))
        item['id'] = cursor.lastrowid
        self.conn.commit()

    def exists(self, cursor, item):
        cursor.execute("""SELECT id FROM car_brand WHERE `name` = '%s'""" % (item['name']))
        id = cursor.fetchone()
        if id is None:
            self.insert(cursor, item)
        else:
            item['id'] = id['id']
