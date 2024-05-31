import pandas as pd
import pymysql
import os
from DatabaseInfo import DatabaseInfo

try:
    mydb = pymysql.connect(host=DatabaseInfo.host, user=DatabaseInfo.user, password=DatabaseInfo.pwd, port=DatabaseInfo.port,database=DatabaseInfo.database)
    # 创建游标对象
    cursor = mydb.cursor()
    # sql = "create table if not exists trainingdata (id int auto_increment primary key ,stu_id varchar(13) comment '学号', x1 decimal(5,2), x2 decimal(5,2), x3 decimal(5,2), x4 decimal(5,2), x5 decimal(5,2), x6 decimal(5,2), x7 decimal(5,2), x8 decimal(5,2), x9 decimal(5,2), x10 decimal(5,2), x11 decimal(5,2), x12 decimal(5,2), y1 varchar(40) comment '单位性质', y2 varchar(40) comment '工作单位',y1_pre varchar(40) comment '预测数据') comment '训练数据';"
    # # sql = "create table if not exists trainingdata (id varchar(13) primary key comment '学号', x1 decimal(5,2), x2 decimal(5,2), x3 decimal(5,2), x4 decimal(5,2), x5 decimal(5,2), x6 decimal(5,2), x7 decimal(5,2), x8 decimal(5,2), x9 decimal(5,2), x10 decimal(5,2), x11 decimal(5,2), x12 decimal(5,2),x13 varchar(10) comment '专业', y1 varchar(40) comment '单位性质', y2 varchar(40) comment '工作单位') comment '训练数据';"
    # cursor.execute(sql)
    # sql='use database employmentprediction'
    # cursor.execute(sql)
    print('连接成功!初始化成功!')
except:
    print("连接失败")
    exit(0)

try:
    sql="insert into {}(year, avg_re1, avg_re2, avg_re3, avg_re4, avg_re5, avg_re6, avg_re7, avg_re8, avg_re9, avg_re10, avg_re11, avg_re12) select year,avg(x1),avg(x2),avg(x3),avg(x4),avg(x5),avg(x6),avg(x7),avg(x8),avg(x9),avg(x10),avg(x11),avg(x12) from {} join {} on {}.stu_id={}.stu_id group by year;".format(DatabaseInfo.statistics,DatabaseInfo.ability,DatabaseInfo.student,DatabaseInfo.ability,DatabaseInfo.student)
    cursor.execute(sql)
except:
    print("statistics已添加逐年统计数据")
try:
    sql="insert into {}(year, avg_re1, avg_re2, avg_re3, avg_re4, avg_re5, avg_re6, avg_re7, avg_re8, avg_re9, avg_re10, avg_re11, avg_re12) select 0,avg(x1),avg(x2),avg(x3),avg(x4),avg(x5),avg(x6),avg(x7),avg(x8),avg(x9),avg(x10),avg(x11),avg(x12) from {} join {} on {}.stu_id={}.stu_id;".format(DatabaseInfo.statistics,DatabaseInfo.ability,DatabaseInfo.student,DatabaseInfo.ability,DatabaseInfo.student)
    cursor.execute(sql)
except:
    print("statistics已添加历史统计数据")
mydb.commit()

try:
    sql='''insert into {} (year,re,value)
    select year,'avg_re1',avg_re1 from {}
    union all
    select year,'avg_re2',avg_re2 from {}
    union all
    select year,'avg_re3',avg_re3 from {}
    union all
    select year,'avg_re4',avg_re4 from {}
    union all
    select year,'avg_re5',avg_re5 from {}
    union all
    select year,'avg_re6',avg_re6 from {}
    union all
    select year,'avg_re7',avg_re7 from {}
    union all
    select year,'avg_re8',avg_re8 from {}
    union all
    select year,'avg_re9',avg_re9 from {}
    union all
    select year,'avg_re10',avg_re10 from {}
    union all
    select year,'avg_re11',avg_re11 from {}
    union all
    select year,'avg_re12',avg_re12 from {}'''.format(DatabaseInfo.statistics_record,DatabaseInfo.statistics,DatabaseInfo.statistics,DatabaseInfo.statistics,DatabaseInfo.statistics,DatabaseInfo.statistics,DatabaseInfo.statistics,DatabaseInfo.statistics,DatabaseInfo.statistics,DatabaseInfo.statistics,DatabaseInfo.statistics,DatabaseInfo.statistics,DatabaseInfo.statistics)
    cursor.execute(sql)
except:
    print("statistics_record已添加数据")
mydb.commit()
# df=pd.read_sql(sql,mydb)
# for row in df: