import pymysql
from DatabaseInfo import DatabaseInfo

# 连接mysql数据库
try:
    mydb = pymysql.connect(host=DatabaseInfo.host, user=DatabaseInfo.user, password=DatabaseInfo.pwd, port=DatabaseInfo.port,database=DatabaseInfo.database)
    # 创建游标对象
    cursor = mydb.cursor()
    print('连接成功!初始化成功!')
except:
    print('连接出错!')
    exit(0)

sql="with unique_stu_id(stu_id) as ((select distinct stu_id from {}) intersect (select distinct stu_id from {}))delete from {} where stu_id not in (select stu_id from unique_stu_id);".format(DatabaseInfo.score,DatabaseInfo.employment,DatabaseInfo.score)
cursor.execute(sql)
sql="with unique_stu_id(stu_id) as ((select distinct stu_id from {}) intersect (select distinct stu_id from {}))delete from {} where stu_id not in (select stu_id from unique_stu_id);".format(DatabaseInfo.score,DatabaseInfo.employment,DatabaseInfo.employment)
cursor.execute(sql)
sql="ALTER TABLE {} AUTO_INCREMENT = 1;".format(DatabaseInfo.employment)
cursor.execute(sql)
sql="ALTER TABLE {} AUTO_INCREMENT = 1;".format(DatabaseInfo.score)
cursor.execute(sql)
# sql=

mydb.commit()
# 关闭游标对象和连接
cursor.close()
mydb.close()