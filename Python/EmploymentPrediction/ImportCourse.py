import os
import pandas as pd
import pymysql
from DatabaseInfo import DatabaseInfo

# 连接mysql数据库
try:
    mydb = pymysql.connect(host=DatabaseInfo.host, user=DatabaseInfo.user, password=DatabaseInfo.pwd, port=DatabaseInfo.port,database=DatabaseInfo.database)
    # 创建游标对象
    cursor = mydb.cursor()
    # # 创建数据库
    # cursor.execute("create database if not exists EmploymentPrediction")
    # cursor.execute("use EmploymentPrediction")
except:
    print('连接出错!')
    exit(0)

# 获取python文件所在目录，并作为根目录
root_dir = os.path.dirname(__file__)
root_dir = ("培养方案/")
excel_files = [f for f in os.listdir(root_dir) if (f.endswith(".xlsx") or f.endswith(".xls"))]

data_frames = {}
course_dp = pd.DataFrame()
result_dp = pd.DataFrame()
for excel_file in excel_files:
    file_path = os.path.join(root_dir, excel_file)
    df = pd.read_excel(file_path)
    df.replace(["H", "h"], 0.6, inplace=True)
    df.replace(["M", "m"], 0.3, inplace=True)
    df.replace(["L", "l"], 0.1, inplace=True)
    df['课程名称'] = df['课程名称'].str.replace("Ⅰ", "I")
    df['课程名称'] = df["课程名称"].str.replace("Ⅱ", "II")
    df['课程名称'] = df["课程名称"].str.replace("Ⅲ", "III")
    df['课程名称'] = df["课程名称"].str.replace("（", "(")
    df['课程名称'] = df["课程名称"].str.replace("）", ")")
    df['课程名称'] = df['课程名称'].str.replace(" ", "")
    df.fillna(0, inplace=True)
    data_frames[excel_file] = df
    course_dp = pd.concat([course_dp, df])
    course_dp = course_dp.drop_duplicates()

# 将课程名称设为行索引，并保留原课程名称列
course_index = course_dp.iloc[:, 0]
course_dp.set_index("课程名称", inplace=True)

course_dp.insert(0, "课程名称", course_dp.index)

data_group = [tuple(x) for x in course_dp.values]

sql = "insert into {} (coursename,re1, re2,re3,re4,re5,re6,re7,re8,re9,re10,re11,re12) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update re1=values(re1), re2=values(re2), re3=values(re3), re4=values(re4), re5=values(re5), re6=values(re6), re7=values(re7), re8=values(re8), re9=values(re9), re10=values(re10), re11=values(re11), re12=values(re12);".format(DatabaseInfo.course)
cursor.executemany(sql, data_group)
mydb.commit()

# 关闭游标对象和连接
cursor.close()
mydb.close()
