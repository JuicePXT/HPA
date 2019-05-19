from Data_processing import db,data_pr
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA

mysql_info=['root','123456','101.132.126.194','3306','house_price']
database=db.Mysql(mysql_info)
clean_data=database.getdata('clean_data')
huxing=data_pr.Process(clean_data,'huxing')
quyu=data_pr.Process(clean_data,'quyu')
louceng=data_pr.Process(clean_data,'louceng')
chaoxiang=data_pr.Process(clean_data,'chaoxiang')
shijian=data_pr.Process(clean_data,'shijian')

#数据规约
clean_data.drop('xiaoqu',axis=1, inplace=True)#删除小区属性
clean_data.drop('danjia',axis=1, inplace=True)#删除单价属性
#数据变化
#定性数据编码化
huxing_namelist=list(huxing.only())
quyu_namelist=list(quyu.only())
louceng_namelist=list(louceng.only())
chaoxiang_namelist=list(chaoxiang.only())
shijian_namelist=list(shijian.only())
le = preprocessing.LabelEncoder()
le.fit(huxing_namelist)
clean_data['huxing']=le.transform(huxing.data)
le.fit(quyu_namelist)
clean_data['quyu']=le.transform(quyu.data)
le.fit(louceng_namelist)
clean_data['louceng']=le.transform(louceng.data)
le.fit(chaoxiang_namelist)
clean_data['chaoxiang']=le.transform(chaoxiang.data)
le.fit(shijian_namelist)
clean_data['shijian']=le.transform(shijian.data)
#主成分分析
pca=PCA()
pca.fit(clean_data.drop('id',axis=1))
#print(pca.components_)#返回模型的各个特征向量
print(pca.explained_variance_ratio_)#返回各个成分各自的方差百分比

database.store_df(clean_data,'preproed_data')
print("数据预处理完成，数据已导入数据库。")
