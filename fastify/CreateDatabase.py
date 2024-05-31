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
sql = "create table if not exists {}(coursename varchar(60) primary key comment '课程名称',re1 decimal(2,1) default 0 comment '毕业要求1', re2 decimal(2,1) default 0 comment '毕业要求2',re3 decimal(2,1) default 0 comment '毕业要求3',re4 decimal(2,1) default 0 comment '毕业要求4',re5 decimal(2,1) default 0 comment '毕业要求5',re6 decimal(2,1) default 0 comment '毕业要求6',re7 decimal(2,1) default 0 comment '毕业要求7',re8 decimal(2,1) default 0 comment '毕业要求8',re9 decimal(2,1) default 0 comment '毕业要求9',re10 decimal(2,1) default 0 comment '毕业要求10',re11 decimal(2,1) default 0 comment '毕业要求11',re12 decimal(2,1) default 0 comment '毕业要求12') comment '课程与毕业要求对应矩阵'".format(DatabaseInfo.course)
cursor.execute(sql)
sql = "create table if not exists {}(id int auto_increment primary key ,stu_id varchar(13) unique comment '学号',name varchar(40) comment '姓名',classname varchar(20) comment '班级',year int comment '入学年份')comment '学生信息表'".format(DatabaseInfo.student)
cursor.execute(sql)
sql = "create table if not exists {}(id int auto_increment primary key ,stu_id varchar(13) unique comment '学号',natureofunit varchar(40) comment '单位性质',workplace varchar(40) comment '工作单位',constraint fk_employment_stu_id foreign key (stu_id) references {}(stu_id) ON DELETE RESTRICT ON UPDATE CASCADE)comment '毕业去向表';".format(DatabaseInfo.employment,DatabaseInfo.student)
cursor.execute(sql)
sql = "create table if not exists {}(id int auto_increment primary key ,stu_id varchar(13) comment '学号', coursename varchar(60) comment '课程名称',natureofexam decimal(2,1) comment '考试性质',credit decimal(4,2) comment '学分',score decimal(5,2) comment '成绩',constraint fk_score_stu_id foreign key (stu_id) references {}(stu_id) ON DELETE RESTRICT ON UPDATE CASCADE,constraint fk_score_coursename foreign key (coursename) references {}(coursename) ON DELETE RESTRICT ON UPDATE CASCADE)comment '成绩表';".format(DatabaseInfo.score,DatabaseInfo.student,DatabaseInfo.course)
cursor.execute(sql)
sql = "create table if not exists {}(id int auto_increment primary key, year int unique comment '年份',avg_re1 decimal(5,2),avg_re2 decimal(5,2),avg_re3 decimal(5,2),avg_re4 decimal(5,2),avg_re5 decimal(5,2),avg_re6 decimal(5,2),avg_re7 decimal(5,2),avg_re8 decimal(5,2),avg_re9 decimal(5,2),avg_re10 decimal(5,2),avg_re11 decimal(5,2),avg_re12 decimal(5,2))comment '能力统计表';".format(DatabaseInfo.statistics)
cursor.execute(sql)
sql = "create table if not exists {}(id int auto_increment primary key, year int comment '年份', re varchar(20) comment '毕业要求',value decimal(5,2),constraint uq_statistics_record_year_re unique (year, re))comment '能力统计数据'".format(DatabaseInfo.statistics_record)
cursor.execute(sql)
sql = "create table if not exists {} (id int auto_increment primary key, stu_id varchar(13) comment '学号', x1 decimal(5,2), x2 decimal(5,2), x3 decimal(5,2), x4 decimal(5,2), x5 decimal(5,2), x6 decimal(5,2), x7 decimal(5,2), x8 decimal(5,2), x9 decimal(5,2), x10 decimal(5,2), x11 decimal(5,2), x12 decimal(5,2), y1 varchar(40) comment '单位性质', y2 varchar(40) comment '工作单位',constraint uq_ability_stu_id unique (stu_id)) comment '能力表';".format(DatabaseInfo.ability)
cursor.execute(sql)
sql = "create table if not exists {} (id int auto_increment primary key , stu_id varchar(13) comment '学号', re varchar(20) comment '毕业要求',value decimal(5,2),constraint fk_ability_record_stu_id foreign key (stu_id) references {}(stu_id),constraint uq_ability_record_stu_id_re unique (stu_id,re))comment '能力数据';".format(DatabaseInfo.ability_record,DatabaseInfo.student)
cursor.execute(sql)
sql = "create table if not exists {} (id int auto_increment primary key ,stu_id  varchar(13) comment '学号', natureofunit varchar(40) comment '去向名称', possibility decimal(5,2) comment '去向对应概率',constraint fk_probability_record_stu_id foreign key (stu_id) references {}(stu_id))comment '去向数据'".format(DatabaseInfo.possibility_record,DatabaseInfo.student)
cursor.execute(sql)

# 关闭游标对象和连接
cursor.close()
mydb.close()