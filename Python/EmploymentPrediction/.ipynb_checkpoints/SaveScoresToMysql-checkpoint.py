import pymysql
import pandas as pd
import numpy as np
import os

natureofexam_white_list = ["缓考"]

# 连接mysql数据库
try:
    mydb = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306)
    # 创建游标对象
    cursor = mydb.cursor()
    # 创建数据库
    cursor.execute("create database if not exists EmploymentPrediction")
    cursor.execute("use EmploymentPrediction")
    cursor.execute(
        "create table if not exists scores(id varchar(13) comment '学号', coursename varchar(60) comment '课程名称',natureofexam decimal(2,1) comment '考试性质',credit decimal(4,2) comment '学分',score decimal(5,2) comment '成绩')comment '成绩表';")
    print('连接成功!初始化成功!')
except:
    print('连接出错!')
    exit(0)

# 获取python文件所在目录，并作为根目录
root_dir = os.path.dirname(__file__)
root_dir = ("数据整理/计网院/计网院 成绩列表/")
excel_files = [f for f in os.listdir(root_dir) if (f.endswith(".xls") or f.endswith(".xlsx"))]

data_frames = {}
for excel_file in excel_files:
    file_path = os.path.join(root_dir, excel_file)
    # header=2 忽略无用的表头
    df = pd.read_excel(file_path, header=2)
    data_frames[excel_file] = df

    # for file_name, df in data_frames.items():
    # file_name = "成绩列表2015级.xls"
    # df = data_frames[file_name]
    # 选取有效信息
    # 0:学号 1:课程名称 2:考试性质 3:学分 4:总成绩 5:成绩标志
    useful_columns = ["学号","课程名称", "考试性质", "学分", "总成绩", "成绩标志"]
    df = df[useful_columns].copy()
    df.drop(df[df["成绩标志"].isin(natureofexam_white_list)].index,inplace=True)
    df.drop(columns = "成绩标志",inplace=True)
    df.replace("优", 95, inplace=True)
    df.replace("良", 85, inplace=True)
    df.replace("中", 75, inplace=True)
    df.replace("及格", 60, inplace=True)
    df.replace("不及格", 50, inplace=True)
    # df['班级名称'].replace('*计算机*','计算机科学与技术',inplace=True)
    # df['班级名称'].replace('*软件*','软件工程',inplace=True)
    # df['班级名称'].replace('*网络*','网络安全',inplace=True)
    df['课程名称'] = df['课程名称'].str.replace("Ⅰ", "I")
    df['课程名称'] = df["课程名称"].str.replace("Ⅱ", "II")
    df['课程名称'] = df["课程名称"].str.replace("Ⅲ", "III")
    df['课程名称'] = df["课程名称"].str.replace("（", "(")
    df['课程名称'] = df["课程名称"].str.replace("）", ")")
    df['课程名称'] = df["课程名称"].str.replace(" ", "")
    df['考试性质'].replace({"正常考试":1, "重.*":0.8, "毕业清考":0.8}, regex=True, inplace=True)
    # df['课程名称'] = df['课程名称'].str.replace("Ⅰ", "I").replace("Ⅱ", "II").replace("Ⅲ", "III").replace("（","(").replace("）", ")").replace(" ", "")
    df["总成绩"].astype(float)
    df.drop_duplicates()
    data_group = [tuple(x) for x in df.values]
    sql = "insert into scores (id,coursename,natureofexam,credit,score) values (%s,%s,%s,%s,%s)"
    cursor.executemany(sql, data_group)
    mydb.commit()

sql = "select distinct id from scores"
# sql="select distinct id,coursename from scores where id=2013550219"
# sql="select * from scores where id=2013550219 and coursename='概率论与数理统计Ⅱ'"
cursor.execute(sql)
# result=cursor.fetchall()
# print(result)

# 关闭游标对象和连接
cursor.close()
mydb.close()
