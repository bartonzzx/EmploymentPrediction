import pymysql
import pandas as pd
import numpy as np
import os
from DatabaseInfo import DatabaseInfo

natureofexam_white_list = ["缓考"]

# 连接mysql数据库
try:
    mydb = pymysql.connect(host=DatabaseInfo.host, user=DatabaseInfo.user, password=DatabaseInfo.pwd, port=DatabaseInfo.port,database=DatabaseInfo.database)
    # 创建游标对象
    cursor = mydb.cursor()
    # 创建数据库
    # cursor.execute("create database if not exists EmploymentPrediction")
    # cursor.execute("use EmploymentPrediction")
    # 禁用外键约束
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    print('连接成功!初始化成功!')
except:
    print('连接出错!')
    exit(0)

# 获取python文件所在目录，并作为根目录
# root_dir = os.path.dirname(__file__)
root_dir = ("数据整理/计网院/计网院 成绩列表/")
excel_files = [f for f in os.listdir(root_dir) if (f.endswith(".xls") or f.endswith(".xlsx"))]

data_frames = {}
for excel_file in excel_files:
    file_path = os.path.join(root_dir, excel_file)
    # header=2 忽略无用的表头
    df = pd.read_excel(file_path, header=2)
    data_frames[excel_file] = df

    # 选取有效信息
    useful_columns = ["学号", "姓名", "班级名称", "课程名称", "考试性质", "学分", "总成绩", "成绩标志"]
    df = df[useful_columns].copy()
    df.drop(df[df["成绩标志"].isin(natureofexam_white_list)].index, inplace=True)
    # df.drop(columns="成绩标志", inplace=True)
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
    df['考试性质'].replace({"正常考试": 1, "重.*": 0.8, "毕业清考": 0.8}, regex=True, inplace=True)
    df["总成绩"].astype(float)
    df.drop_duplicates(inplace=True)

    df_student=df.loc[:,["学号", "姓名", "班级名称"]].copy()
    df_student['入学年份']=df_student['学号'].astype(str).str[:4]
    df_student.drop_duplicates(inplace=True)

    data_student_group=[tuple(x) for x in df_student.values]
    sql="insert into {} (stu_id,name,classname,year) values (%s,%s,%s,%s) on duplicate key update name=values(name), classname=values(classname), year=values(year);".format(DatabaseInfo.student)
    sql=cursor.executemany(sql,data_student_group)
    mydb.commit()
    data_score_group = [tuple(x) for x in df.loc[:,["学号", "课程名称", "考试性质", "学分", "总成绩"]].values]
    sql = "insert into {} (stu_id,coursename,natureofexam,credit,score) values (%s,%s,%s,%s,%s)".format(DatabaseInfo.score)
    cursor.executemany(sql, data_score_group)
    mydb.commit()

# # 删除无对应就业数据的成绩
# cursor.execute(
#     "delete from scores where stu_id not in (select stu_id from employment);"
# )
# mydb.commit()

# 删除无对应毕业要求的成绩
# cursor.execute(
#     "delete from score where coursename not in (select coursename from course);"
# )
# mydb.commit()
# 启用外键约束
cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
mydb.commit()

sql = "select distinct id from {}".format(DatabaseInfo.score)
cursor.execute(sql)

# 关闭游标对象和连接
cursor.close()
mydb.close()
