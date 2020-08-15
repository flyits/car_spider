#!/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect(host='car_mysql',
                     db='car_spider',
                     user='root',
                     password='root', )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句
sql = "SELECT id FROM car_model \
       WHERE `name` = '%s'" % ('爱驰U5')
# 执行SQL语句
cursor.execute(sql)
id = cursor.fetchone()
if  id is not None:
    print(id[0])
else:
    print('can Insert')
# data是元组，试着转换成list，允许修改，这样后面阶段的事情比较容易处理
print('show databases执行完毕\n')


# 关闭数据库连接
db.close()
