import numpy as np
import pandas as pd
import pymysql
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.decomposition import PCA

# 连接mysql数据库
try:
    mydb = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306, database='employmentprediction')
    # 创建游标对象
    cursor = mydb.cursor()
    print('连接成功!初始化成功!')
except:
    print('连接出错!')
    exit(0)

sql = "select * from trainingdata;"
data = pd.read_sql(sql, mydb)

data.set_index('id', inplace=True)
# data.drop(columns='x13',inplace=True)
# data.drop(columns='y2',inplace=True)

data.replace(['医疗卫生单位', '城镇社区', '其他教学单位', '其他教学单位', '其他事业单位', '机关'], '事业单位',
             inplace=True)
data.replace('出国、出境深造', '升学', inplace=True)
data.replace(['其他暂不就业', '不就业拟升学'], '待就业', inplace=True)
data.replace(['国家基层项目', '地方基层项目'], '事业单位', inplace=True)
data.replace(['科研设计单位', '科研助理', '高等学校'], '高校教科研事业', inplace=True)
data.replace(['国有企业', '三资企业'], '国有、三资企业', inplace=True)
data = data[~data['y1'].isin(['自主创业', '部队'])]

# data.replace(['其他企业','国有、三资企业及事业单位','自由职业','高校教科研事业','升学'],'就业',inplace=True)


y1_label_encoder = LabelEncoder()
data['y1_label_encoded'] = y1_label_encoder.fit_transform(data['y1'])

y_1hot_encoder = OneHotEncoder()
y_1hot = y_1hot_encoder.fit_transform(data['y1_label_encoded'].values.reshape(-1, 1))

x13_label_encoder = LabelEncoder()
data['x13_label_encoded'] = x13_label_encoder.fit_transform(data['x13'])

x13_1hot_encoder = OneHotEncoder()
x13_1hot = x13_1hot_encoder.fit_transform(data['x13_label_encoded'].values.reshape(-1, 1))

data_encoded = pd.concat(
    [data.reset_index(drop=True), pd.DataFrame(x13_1hot.toarray(), columns=x13_label_encoder.classes_),
     pd.DataFrame(y_1hot.toarray(), columns=y1_label_encoder.classes_)], axis=1)

X = data_encoded.drop(
    ['x13', 'x13_label_encoded', 'y1', 'y1_label_encoded', 'y2'] + list(x13_label_encoder.classes_) + list(
        y1_label_encoder.classes_), axis=1)
y = data_encoded[y1_label_encoder.classes_]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# 标准化
# scaler = StandardScaler()
# scaled_X = scaler.fit_transform(X)
X_y = data_encoded.drop(['x13','x13_label_encoded','y1', 'y1_label_encoded', 'y2'], axis=1)
# X_y[['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12']] = scaled_X

# 主成分分析降维+居中
# pca = PCA(n_components=12)

# 创建列名列表
# x_pca_columns = {x:"x{}".format(x) for x in range(pca.n_components)}

# X6D = pca.fit_transform(X)
# X6D_df = pd.DataFrame(X6D).rename(columns=x_pca_columns)
# X_y = pd.concat([X6D_df,data_encoded[list(x13_label_encoder.classes_) + list(y1_label_encoder.classes_)].reset_index(drop=True)], axis=1)

corr_matrix = []
y_list = ['其他企业', '升学', '国有、三资企业', '待就业', '自由职业', '高校教科研事业', '事业单位']
for index in range(7):
    y_todel = y_list[index]
    temp_y = y_list[:index] + y_list[index + 1:]
    corr_matrix.append(X_y.drop(columns=temp_y, axis=1).corr())

# 分层抽样
split = StratifiedShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
for train_index, test_index in split.split(X_y, y):
    strat_train_set = X_y.loc[train_index]
    strat_test_set = X_y.loc[test_index]

X_train=strat_train_set.drop(list(y1_label_encoder.classes_), axis=1)
y_train=strat_train_set[list(y1_label_encoder.classes_)]
X_test=strat_test_set.drop(list(y1_label_encoder.classes_), axis=1)
y_test=strat_test_set[list(y1_label_encoder.classes_)]


# 训练决策树模型
# model = KNeighborsClassifier()
model = RandomForestClassifier(criterion='gini'
                               ,split="random"
                               ,random_state=42)
model.fit(X_train,y_train)

# y_train_pred = cross_val_predict(model, X_train, y_train, cv=10)
# y_train_score = cross_val_score(model, X_train, y_train, cv=10, scoring='accuracy')
# print("cross validation accuracy"+y_train_pred)
# confusion_mx = confusion_matrix(y_train[], y_train_pred)

# print(confusion_mx)

# 预测测试集
y_pred = model.predict(X_test)
#
# 计算准确率
accuracy = accuracy_score(strat_test_set[list(y1_label_encoder.classes_)], y_pred)
print("准确率:", accuracy)

# 关闭游标对象和连接
cursor.close()
mydb.close()
