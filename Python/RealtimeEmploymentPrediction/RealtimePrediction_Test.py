import joblib
import numpy as np
import pandas as pd
import pymysql
from metric_learn import LMNN
from sklearn.base import clone
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OrdinalEncoder
from sklearn.utils import shuffle
from sklearn.ensemble import VotingClassifier
# from combo.models.classifier_stacking import Stacking
from combo.models.classifier_comb import SimpleClassifierAggregator
from DatabaseInfo import DatabaseInfo
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from imblearn.metrics import geometric_mean_score
from sklearn.datasets import load_wine
from ucimlrepo import fetch_ucirepo

try:
    mydb = pymysql.connect(host=DatabaseInfo.host, user=DatabaseInfo.user, password=DatabaseInfo.pwd,
                           port=DatabaseInfo.port, database=DatabaseInfo.database)
    cursor = mydb.cursor()
    print('初始化成功！连接成功！')
except:
    print('连接出错')
    exit(0)


class imclassifier:
    """在不平衡数据集中进行分类预测"""

    def __init__(self, data_original, feature_name, label_name, ir_threshold=4, knn_neighbors=5, learn_rate=1e-6,
                 dsc=True, dse=True,
                 dfe=True, csl=True,
                 el=True):
        """data_original存储原始数据"""
        self.data_original = data_original

        'feature存储data_original中的特征列名'
        self.feature_name = feature_name

        'label存储data_original中的标签列名'
        self.label_name = label_name

        self.knn_neighbors = knn_neighbors
        self.learn_rate = learn_rate

        '''
        标签占比阈值,
        如果标签的占比大于阈值,
        这个标签才会被选入筛选器
        '''
        # self.target_threshold=target_threshold

        'IR阈值'
        self.ir_threshold = ir_threshold

        '变换同义的标签'
        # self.data_original[label].replace(['其他暂不就业','不就业拟升学'],value='待就业',inplace=True)

        #         '对原始数据的标签进行统计'
        #         self.target_counts=self.data_original[self.label_name].value_counts(normalize=True)

        #         'target_selected是index属性的,用此来筛选数据'
        #         self.target_selected=self.target_counts[self.target_counts>=self.target_threshold].index

        #         'data_selected用于存储筛选后的数据'
        #         self.data_selected=self.data_original[self.data_original[self.label_name].isin(self.target_selected)]

        'feature用于存储所有的特征'
        self.feature = self.data_original.loc[:, self.feature_name]
        'target用于存储标签'
        self.target = self.data_original.loc[:, self.label_name]

        '为标签列编码'
        self.target_o_encoder = OrdinalEncoder()
        self.target_ordinal = pd.DataFrame(self.target_o_encoder.fit_transform(self.target.to_frame()),
                                           columns=[self.label_name])

        # self.target_ordinal = pd.DataFrame(self.target_o_encoder.fit_transform(self.target),
        #                                    columns=[self.label_name])

        '编码器编码的标签名,target_name为数组属性'
        self.target_name = self.target_o_encoder.categories_[0]

        '经由编码器编码后的总标签数'
        self.target_types = len(self.target_name)

        '''
        DSC:Data Subset Construction
        data_subset用于存储子数据集
        data_subset_ir用于存储子数据集imbalance ratio
        '''
        self.data_subset = []
        self.data_subset_ir = []
        self.data_subset_value_counts = []
        if dsc:
            self.dsc()
        else:
            self.nodsc()
        'DSE:Data Subset Extension'
        self.data_subset_extension = []
        if dse:
            self.dse()
        else:
            self.nodse()
        'DFE:Data Feature Emphasis'
        self.data_subset_extension_emphasis = []
        self.data_subset_lmnn = []
        if dfe:
            self.dfe()
        # else:
        #     self.nodfe()

        'BC:Base Classifier'
        self.data_subset_bc = []
        if el:
            self.bc()
        # 'CSL:Cost-Sensitive Learning'
        # self.data_subset_csl = []
        # if csl:
        #     self.csl()

        'EL:Ensemble Learning'
        self.data_subset_el = []
        if el:
            self.el()

    '自定义权重'

    def custom_weights(distances, y_train):
        # 获取每个样本点的 k 个最近邻的标签
        knn_labels = y_train[np.argsort(distances)[:, :5]]

        # 统计每个样本点附近两类样本的数量差异
        diff = np.abs(np.sum(knn_labels == 0, axis=1) - np.sum(knn_labels == 1, axis=1))

        # 根据数量差异赋予样本点不同的权重
        weights = np.where(diff <= 2, 0.5, 2.0)

        return weights

    'DSC:Data Subset Construction'

    def dsc(self):
        for index in range(self.target_types):
            temp_df = pd.concat([self.feature, self.target_ordinal], axis='columns', join='inner')

            # print(temp_df)
            # print(temp_df.loc[:,self.label_name])

            temp_df[self.label_name] = np.where(temp_df[self.label_name] == index, 1, 0)

            self.data_subset_value_counts.append(temp_df[self.label_name].value_counts())

            self.data_subset.append(temp_df)
            self.data_subset_ir.append(
                self.data_subset_value_counts[index][0] / self.data_subset_value_counts[index][1])

    'NODSC:No Data Subset Construction'

    def nodsc(self):
        temp_df = pd.concat([self.feature, self.target_ordinal], axis='columns', join='inner')
        temp_value_counts = temp_df[self.label_name].value_counts()
        self.data_subset.append(temp_df)
        self.data_subset_ir.append(temp_value_counts[0] / temp_value_counts[1])

    'DSE:Data Subset Extension'

    def dse(self):
        for index in range(len(self.data_subset)):
            temp_data_subset_extension = []
            if self.data_subset_ir[index] >= self.ir_threshold:
                data_subset_extension_minor_size = self.data_subset_value_counts[1]
                data_subset_extension_major_minor_ratio = round(
                    self.data_subset_value_counts[index][0] / self.data_subset_value_counts[index][1])
                # print(data_subset_extension_major_minor_ratio)

                minor_data = self.data_subset[index][self.data_subset[index][self.label_name] == 1]
                major_data = self.data_subset[index][self.data_subset[index][self.label_name] == 0]

                major_data_shuffled = shuffle(major_data)

                '进行划分,若数据不够进行一次划分则全部选用'
                major_chunks = np.array_split(major_data_shuffled, data_subset_extension_major_minor_ratio)
                for major_chunk in major_chunks:
                    temp_data_subset_extension_base = pd.concat([minor_data, major_chunk])
                    temp_data_subset_extension.append(temp_data_subset_extension_base)
            else:
                temp_data_subset_extension.append(self.data_subset[index])

            self.data_subset_extension.append(temp_data_subset_extension)

    'NODSE:No Data Subset Extension'

    def nodse(self):
        for index in range(len(self.data_subset)):
            temp_data_subset_extension = []
            temp_data_subset_extension.append(self.data_subset[index])
            self.data_subset_extension.append(temp_data_subset_extension)

    'DFE:Data Feature Emphasis'

    def dfe(self):
        for index in range(len(self.data_subset_extension)):
            temp_subset_lmnn = LMNN(n_neighbors=self.knn_neighbors, learn_rate=1e-6, random_state=42)
            temp_subset_lmnn.fit(self.data_subset[index].loc[:, self.feature_name],
                                 self.data_subset[index].loc[:, self.label_name])

            self.data_subset_lmnn.append(temp_subset_lmnn)

            temp_data_subset_extension_emphasis = []

            for index_1 in range(len(self.data_subset_extension[index])):
                temp_data = self.data_subset_extension[index][index_1]
                temp_x = temp_data.loc[:, self.feature_name]
                temp_y = temp_data.loc[:, self.label_name]

                temp_x_lmnn = temp_subset_lmnn.transform(temp_x)
                temp_data_subset_extension_emphasis.append(
                    pd.concat([pd.DataFrame(temp_x_lmnn, columns=self.feature_name), temp_y.reset_index(drop=True)],
                              axis=1))

            self.data_subset_extension_emphasis.append(temp_data_subset_extension_emphasis)

    def nodfe(self):
        self.data_subset_extension_emphasis = self.data_subset_extension

    'BC:Base Classifier'

    def bc(self):
        for index in range(len(self.data_subset_extension_emphasis)):
            temp_subset_bc = []
            for index_1 in range(len(self.data_subset_extension_emphasis[index])):
                temp_bc = KNeighborsClassifier(n_neighbors=self.knn_neighbors, weights='distance', n_jobs=-1)
                # temp_knn = KNeighborsClassifier(n_neighbors=5,weights=self.custom_weights)
                temp_bc.fit(self.data_subset_extension_emphasis[index][index_1].loc[:, self.feature_name],
                            self.data_subset_extension_emphasis[index][index_1].loc[:, self.label_name])

                # print(temp_bc.score(
                #     self.data_subset_extension_emphasis[index][index_1].loc[:, self.feature_name],
                #     self.data_subset_extension_emphasis[index][index_1].loc[:, self.label_name]))
                # print(temp_knn.score(self.data_subset_extension_emphasis[index][index_1].loc[:,self.feature_name],self.data_subset_extension_emphasis[index][index_1].loc[:,self.label_name]))
                # temp_knn=('knn{}'.format(index_1),temp_knn)
                temp_subset_bc.append(temp_bc)
            self.data_subset_bc.append(temp_subset_bc)

    'CSL:Cost-Sensitive Learning'
    '效果太差'
    # def bc(self):
    #     for index in range(len(self.data_subset_extension_emphasis)):
    #         temp_subset_bc = []
    #         for index_1 in range(len(self.data_subset_extension_emphasis[index])):
    #             temp_knn = KNeighborsClassifier(n_neighbors=5)
    #             a = 1
    #             b = 1
    #             temp_cost = np.array([[0, a], [b, 0]])
    #             # print(self.data_subset_extension_emphasis[index][index_1])
    #             temp_csl = MetaCost(self.data_subset_extension_emphasis[index][index_1], temp_knn, temp_cost).fit(
    #                 self.label_name, len(self.label_name))
    #             temp_subset_bc.append(temp_csl)
    #
    #         self.data_subset_bc.append(temp_subset_bc)

    'EL:Ensemble Learning'

    def el(self):
        for index in range(len(self.data_subset_extension_emphasis)):
            if len(self.data_subset_bc[index]) <= 1:
                temp_el = self.data_subset_bc[index][0]
            else:
                temp_el = SimpleClassifierAggregator(self.data_subset_bc[index], method='average', pre_fitted=True)
            # self.temp_data=pd.DataFrame()
            # for index_1 in range(len(self.data_subset_extension_emphasis[index])):
            #     self.temp_data=pd.concat([self.temp_data,self.data_subset_extension_emphasis[index][index_1]],axis=0)
            # temp_el=VotingClassifier(estimators=self.data_subset_csl[index],voting='soft',n_jobs=-1)
            # # temp_el.set_params('drop')
            # temp_el.fit(self.temp_data.loc[:,self.feature_name],self.temp_data.loc[:,self.label_name])
            self.data_subset_el.append(temp_el)

    def predict_proba(self, data_to_predict):
        prediction_result = []
        prediction_proba = []
        for i in range(len(self.data_subset_el)):
            prediction_result.append(
                self.data_subset_el[i].predict(
                    self.data_subset_lmnn[i].transform(data_to_predict.loc[:, self.feature_name])))
            prediction_proba.append(
                self.data_subset_el[i].predict_proba(
                    self.data_subset_lmnn[i].transform(data_to_predict.loc[:, self.feature_name])))
            prediction_proba[i] = prediction_proba[i] * 100

        return prediction_proba

def imsplit(data_original, label_name, target_threshold=0.03):
    '对原始数据的标签进行统计'
    target_counts = data_original[label_name].value_counts(normalize=True)

    'target_selected是index属性的,用此来筛选数据'
    target_selected = target_counts[target_counts >= target_threshold].index

    'data_selected用于存储筛选后的数据'
    data_selected = data_original[data_original[label_name].isin(target_selected)]

    return data_selected


sql = 'select * from {};'.format(DatabaseInfo.realtime_ability)
data_ori = pd.read_sql(sql, mydb)

sql = "delete from {}".format(DatabaseInfo.realtime_possibility_record)
cursor.execute(sql)

data_ori = imsplit(data_ori, label_name='y1', target_threshold=0.03)
data_train, data_test = train_test_split(data_ori, test_size=0.3, random_state=42)
imc = imclassifier(data_train, feature_name=['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12'],
                   label_name='y1', ir_threshold=1, dsc=True, dse=True)

# joblib.dump(imc, 'imclassifier_model.pkl')

data_to_predict = data_test

predictor = imc.data_subset_el

prediction_result = []
prediction_proba = []
for i in range(len(predictor)):
    # for j in range(len(ans[i])):
    # ans_data.append(ans[i].predict_proba(imc.data_subset_lmnn[i].transform(data_test.loc[:,imc.feature_name])))
    # print("catgory {}:{}".format(i, imc.target_name[i]))
    #
    # print(predictor[i].predict(imc.data_subset_lmnn[i].transform(data_test.loc[:, imc.feature_name])))
    prediction_result.append(
        predictor[i].predict(imc.data_subset_lmnn[i].transform(data_to_predict.loc[:, imc.feature_name])))
    prediction_proba.append(
        predictor[i].predict_proba(imc.data_subset_lmnn[i].transform(data_to_predict.loc[:, imc.feature_name])))
    prediction_proba[i] = prediction_proba[i] * 100

prediction_accuracy_score = []
prediction_recall_score = []
prediction_f1_score = []
prediction_precision_score = []
prediction_roc_auc_score = []
prediction_g_mean = []
for i in range(len(predictor)):
    label = imc.target_name[i]
    temp_data = np.where(data_to_predict[imc.label_name] == label, 1, 0)

    prediction_f1_score.append(f1_score(temp_data, prediction_result[i]))
    prediction_recall_score.append(recall_score(temp_data, prediction_result[i]))
    prediction_precision_score.append(precision_score(temp_data, prediction_result[i]))
    prediction_accuracy_score.append(accuracy_score(temp_data, prediction_result[i]))
    prediction_roc_auc_score.append(roc_auc_score(temp_data, prediction_result[i]))
    prediction_g_mean.append(geometric_mean_score(temp_data, prediction_result[i]))

# score={}
print(imc.knn_neighbors)
score = {"g_mean": np.mean(prediction_g_mean), "f1_score": np.mean(prediction_f1_score),
         "auc_score": np.mean(prediction_roc_auc_score), "racall_score": np.mean(prediction_recall_score),
         "accuracy_score": np.mean(prediction_accuracy_score)}
# 遍历键和值
for key, value in score.items():
    print(key + ": " + str(value))

'存储到数据库'
data_predict_result = []
for i in range(len(predictor)):
    label = imc.target_name[i]
    temp_result = pd.concat(
        [data_to_predict.reset_index(drop=True), pd.DataFrame(prediction_proba[i].reshape(-1, 1), columns=[label])],
        axis=1)
    data_predict_result.append(temp_result)

    data_result_group = [tuple([x[0], label, x[1]]) for x in
                         temp_result.loc[:, ['stu_id', label]].values]
    sql = "insert into {}(stu_id,natureofunit,possibility) values(%s,%s,%s)".format(DatabaseInfo.possibility_record)
    cursor.executemany(sql, data_result_group)
    mydb.commit()

cursor.close()
mydb.close()
