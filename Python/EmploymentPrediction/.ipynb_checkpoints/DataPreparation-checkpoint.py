import pymysql
from Student import Student
import pandas as pd

course_white_list = ['程序设计实践']

# 连接mysql数据库
try:
    mydb = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306, database='employmentprediction')
    # 创建游标对象
    cursor = mydb.cursor()
    sql = "create table if not exists trainingdata (id varchar(13) primary key comment '学号', x1 decimal(5,2), x2 decimal(5,2), x3 decimal(5,2), x4 decimal(5,2), x5 decimal(5,2), x6 decimal(5,2), x7 decimal(5,2), x8 decimal(5,2), x9 decimal(5,2), x10 decimal(5,2), x11 decimal(5,2), x12 decimal(5,2), y1 varchar(40) comment '单位性质', y2 varchar(40) comment '工作单位') comment '训练数据';"
    # sql = "create table if not exists trainingdata (id varchar(13) primary key comment '学号', x1 decimal(5,2), x2 decimal(5,2), x3 decimal(5,2), x4 decimal(5,2), x5 decimal(5,2), x6 decimal(5,2), x7 decimal(5,2), x8 decimal(5,2), x9 decimal(5,2), x10 decimal(5,2), x11 decimal(5,2), x12 decimal(5,2),x13 varchar(10) comment '专业', y1 varchar(40) comment '单位性质', y2 varchar(40) comment '工作单位') comment '训练数据';"
    cursor.execute(sql)
    print('连接成功!初始化成功!')
except:
    print('连接出错!')
    exit(0)

# 创建对象数组
    # 获取所有id
sql = "select id from employment;"
cursor.execute(sql)
ids = cursor.fetchall()

# students = {}
students = []
sql = "select * from courses;"
course_dp = pd.read_sql_query(sql, mydb)
course_dp.set_index("coursename",inplace=True)

# ids = (('2014550620',),('2015550842',),('201805820908',))

for id in ids:
    sql = "select natureofunit,workplace from employment where id = %s;"
    # sql = "select natureofunit,workplace,major from employment where id = %s;"
    cursor.execute(sql,(id,))
    result = cursor.fetchone()

    natureofunit = result[0]
    workplace = result[1]
    # major = result[2]
    # students[id[0]]=Student(id[0],natureofunit,workplace)
    students.append(Student(id[0],natureofunit,workplace))
    # students.append(Student(id[0],natureofunit,workplace,major))

    sql = "select * from scores where id = {} and coursename in (select coursename from courses);".format(id[0])
    # 该id全部的成绩数据
    id_all_scores = pd.read_sql_query(sql,mydb)

    # 该id参加的全部课程名称
    id_coursename = list(set(id_all_scores['coursename']))

    # 该id参与的全部课程对应的毕业能力矩阵
    id_course_re = course_dp.loc[id_coursename]

    for re in range(1,13):
        temp_course = id_course_re["graduationre{}".format(re)][id_course_re["graduationre{}".format(re)]!=0]

        # 该id参与的 属于当前毕业要求的 全部课程
        id_re_coursename = temp_course.index.tolist()

        # 该id参与的 属于当前毕业要求的 全部课程的 成绩
        id_re_scores = id_all_scores[id_all_scores['coursename'].isin(id_re_coursename)]

        # 施加重考重修成绩惩罚机制的白名单
        id_re_scores.loc[id_re_scores['coursename'].isin(course_white_list), 'natureofexam'] = 1

        # 添加对应课程的权值
        id_re_scores = pd.merge(left=id_re_scores,right=temp_course,on="coursename",how="inner")

        # 计算成绩加权和的分子
        id_re_scores["weightsum"] = id_re_scores['credit'] * id_re_scores['score'] * id_re_scores['graduationre{}'.format(re)] * id_re_scores['natureofexam']

        # 计算成绩加权和的分母
        weight_sum = sum(id_re_scores['credit'] * id_re_scores['graduationre{}'.format(re)])

        # 当前毕业要求的评分
        try:
            re_score = sum(id_re_scores['weightsum']) / weight_sum
        except ZeroDivisionError:
            del students[-1]
            continue

        # 存储数据
        # students[id[0]].scores['re{}'.format(re)] = re_score
        # students[id[0]].courses['re{}'.format(re)] = id_re_coursename
        students[-1].scores['re{}'.format(re)] = re_score
        students[-1].courses['re{}'.format(re)] = id_re_coursename


        print("graduation req{}:".format(re),re_score)


data_group = [tuple([x.id] + [*x.scores.values()] + [x.natureofunit] + [x.workplace]) for x in students]
# data_group = [tuple([x.id] + [*x.scores.values()] + [x.major] + [x.natureofunit] + [x.workplace]) for x in students]
sql = 'insert into trainingdata (id,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,y1,y2) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
# sql = 'insert into trainingdata (id,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,y1,y2) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
cursor.executemany(sql,data_group)
mydb.commit()

# 关闭游标对象和连接
cursor.close()
mydb.close()