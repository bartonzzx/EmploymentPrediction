import pymysql
import pandas as pd
import os

# 连接mysql数据库
try:
    mydb = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306)
    # 创建游标对象
    cursor = mydb.cursor()
    # 创建数据库
    cursor.execute("create database if not exists EmploymentPrediction")
    cursor.execute("use EmploymentPrediction")
    cursor.execute(
        "create table if not exists employment(id varchar(13) primary key comment '学号',major varchar(10) comment '专业', natureofunit varchar(40) comment '单位性质',workplace varchar(40) comment '工作单位')comment '毕业去向表';")
    print('连接成功!初始化成功!')
except:
    print('连接出错!')
    exit(0)

# 获取python文件所在目录，并作为根目录
# root_dir = os.path.dirname(__file__)
root_dir = ("数据整理/计网院/计算机 19-22届毕业生去向/")
excel_files = [f for f in os.listdir(root_dir) if (f.endswith(".xls") or f.endswith(".xlsx") or f.endswith(".htm"))]

data_frames = {}
for excel_file in excel_files:
    file_path = os.path.join(root_dir, excel_file)
    # 无header 没有额外表头
    # if excel_file.endswith(".xls") or excel_file.endswith("xlsx"):
    try:
        df = pd.read_excel(file_path)
    except:
        df = pd.read_html(file_path, header=0)
    data_frames[excel_file] = df

    if isinstance(df, list):
        df = df[0]
    # 选取有效信息
    # 0:学号 1:单位性质 2:实际工作单位
    id_data = df["学号"]
    df.fillna('', inplace=True)

    major_data = df['专业']

    natureofunit_col = df.columns[df.columns.str.contains("单位性质")]
    if natureofunit_col.size != 0:
        natureofunit_data = df[natureofunit_col].squeeze()
    else:
        natureofunit_data = pd.Series(index=id_data.index)
        natureofunit_data.fillna('', inplace=True)

    workplace_col = df.columns[df.columns.str.contains("实际工作单位")]
    if workplace_col.size != 0:
        workplace_data = df[workplace_col].squeeze()
    else:
        workplace_data = pd.Series(index=id_data.index)
        workplace_data.fillna('', inplace=True)

    data_group = pd.concat([id_data,major_data, natureofunit_data, workplace_data], axis=1)
    df.drop_duplicates()
    data_group = [tuple(x) for x in data_group.values]
    sql = "insert into employment (id, major,natureofunit, workplace) values (%s,%s, %s, %s) on duplicate key update natureofunit=values(natureofunit), workplace=values(workplace)"
    cursor.executemany(sql, data_group)
    mydb.commit()

sql = "select natureofunit from employment"
# sql="select distinct id,coursename from scores where id=2013550219"
# sql="select * from scores where id=2013550219 and coursename='概率论与数理统计Ⅱ'"
cursor.execute(sql)
result = cursor.fetchall()
print(result)
unique = set(result)
print("共有{}种去向".format(len(unique)))

counts = {data: result.count(data) for data in unique}
for data, count in counts.items():
    print("数据 '{}' 有 {} 个".format(data, count))

# 关闭游标对象和连接
cursor.close()
mydb.close()
