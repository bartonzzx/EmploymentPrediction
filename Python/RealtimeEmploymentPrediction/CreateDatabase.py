import pymysql
from DatabaseInfo import DatabaseInfo

try:
    mydb = pymysql.connect(host=DatabaseInfo.host, user=DatabaseInfo.user, password=DatabaseInfo.pwd, port=DatabaseInfo.port,database=DatabaseInfo.database)
    # 创建游标对象
    cursor = mydb.cursor()
    # 创建数据库
    # cursor.execute("create database if not exists EmploymentPrediction")
    # cursor.execute("use EmploymentPrediction")
except:
    print('连接出错!')
    exit(0)

# 创建表
sql = "create table if not exists {}(id int auto_increment primary key ,stu_id varchar(13) unique comment '学号',name varchar(40) comment '姓名',classname varchar(20) comment '班级',year int comment '入学年份')comment '学生信息表'".format(DatabaseInfo.realtime_student)
cursor.execute(sql)
sql = "create table if not exists {}(id int auto_increment primary key ,stu_id varchar(13) comment '学号', coursename varchar(60) comment '课程名称',natureofexam decimal(2,1) comment '考试性质',credit decimal(4,2) comment '学分',score decimal(5,2) comment '成绩',constraint fk_realtime_score_stu_id foreign key (stu_id) references {}(stu_id) ON DELETE RESTRICT ON UPDATE CASCADE)comment '成绩表';".format(DatabaseInfo.realtime_score,DatabaseInfo.realtime_student,DatabaseInfo.course)
cursor.execute(sql)
sql = "create table if not exists {} (id int auto_increment primary key, stu_id varchar(13) comment '学号', x1 decimal(5,2), x2 decimal(5,2), x3 decimal(5,2), x4 decimal(5,2), x5 decimal(5,2), x6 decimal(5,2), x7 decimal(5,2), x8 decimal(5,2), x9 decimal(5,2), x10 decimal(5,2), x11 decimal(5,2), x12 decimal(5,2)) comment '能力表';".format(DatabaseInfo.realtime_ability)
cursor.execute(sql)
sql = "create table if not exists {} (id int auto_increment primary key ,stu_id  varchar(13) comment '学号', natureofunit varchar(40) comment '去向名称', possibility decimal(5,2) comment '去向对应概率',constraint fk_realtime_probability_record_stu_id foreign key (stu_id) references {}(stu_id))comment '去向数据'".format(DatabaseInfo.realtime_possibility_record,DatabaseInfo.realtime_student)
cursor.execute(sql)

# 关闭游标对象和连接
cursor.close()
mydb.close()