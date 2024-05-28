import pymysql
from Student import Student
import pandas as pd
from DatabaseInfo import DatabaseInfo

course_white_list = ['程序设计实践']

# 连接mysql数据库
try:
    mydb = pymysql.connect(host=DatabaseInfo.host, user=DatabaseInfo.user, password=DatabaseInfo.pwd, port=DatabaseInfo.port,database=DatabaseInfo.database)
    # 创建游标对象
    cursor = mydb.cursor()
    print('连接成功!初始化成功!')
except:
    print('连接出错!')
    exit(0)

# 创建对象数组
    # 获取所有id
sql = "select stu_id from {};".format(DatabaseInfo.realtime_student)
cursor.execute(sql)
stu_ids = cursor.fetchall()

# students = {}
students = []
sql = "select * from {};".format(DatabaseInfo.course)
course_dp = pd.read_sql_query(sql, mydb)
course_dp.set_index("coursename",inplace=True)

# stu_ids = (('2014550620',),('2015550842',),('201805820908',))

for stu_id in stu_ids:
    students.append(Student(stu_id[0]))

    sql = "select * from {} where stu_id = {} and coursename in (select coursename from {});".format(DatabaseInfo.realtime_score,stu_id[0],DatabaseInfo.course)
    # 该id全部的成绩数据
    stu_id_all_scores = pd.read_sql_query(sql,mydb)

    # 该id参加的全部课程名称
    stu_id_coursename = list(set(stu_id_all_scores['coursename']))

    # 该id参与的全部课程对应的毕业能力矩阵
    stu_id_course_re = course_dp.loc[stu_id_coursename]

    for re in range(1,13):
        temp_course = stu_id_course_re["re{}".format(re)][stu_id_course_re["re{}".format(re)]!=0]

        # 该id参与的 属于当前毕业要求的 全部课程
        stu_id_re_coursename = temp_course.index.tolist()

        # 该id参与的 属于当前毕业要求的 全部课程的 成绩
        stu_id_re_scores = stu_id_all_scores[stu_id_all_scores['coursename'].isin(stu_id_re_coursename)]

        # 施加重考重修成绩惩罚机制的白名单
        stu_id_re_scores.loc[stu_id_re_scores['coursename'].isin(course_white_list), 'natureofexam'] = 1

        # 添加对应课程的权值
        stu_id_re_scores = pd.merge(left=stu_id_re_scores,right=temp_course,on="coursename",how="inner")

        # 计算成绩加权和的分子
        stu_id_re_scores["weightsum"] = stu_id_re_scores['credit'] * stu_id_re_scores['score'] * stu_id_re_scores['re{}'.format(re)] * stu_id_re_scores['natureofexam']

        # 计算成绩加权和的分母
        weight_sum = sum(stu_id_re_scores['credit'] * stu_id_re_scores['re{}'.format(re)])

        # 当前毕业要求的评分
        try:
            re_score = sum(stu_id_re_scores['weightsum']) / weight_sum
        except ZeroDivisionError:
            del students[-1]
            continue

        # 存储数据
        students[-1].scores['re{}'.format(re)] = re_score
        students[-1].courses['re{}'.format(re)] = stu_id_re_coursename

        print("graduation req{}:".format(re),re_score)

data_ability_record_group=[]
for x in students:
    for key,values in x.scores.items():
        data_ability_record_temp=tuple([x.id]+[key]+[values])
        data_ability_record_group.append(data_ability_record_temp)
data_ability_group = [tuple([x.id] + [*x.scores.values()]) for x in students]
# sql = "insert into {} (stu_id,re,value) values (%s,%s,%s);".format(DatabaseInfo.ability_record)
# cursor.executemany(sql,data_ability_record_group)
sql = 'insert into {} (stu_id,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'.format(DatabaseInfo.realtime_ability)
cursor.executemany(sql,data_ability_group)
mydb.commit()

# 关闭游标对象和连接
cursor.close()
mydb.close()