from Data_processing import db,data_pr
import numpy as np
import numpy as np
from sklearn.model_selection import train_test_split,cross_val_predict
from sklearn.metrics import r2_score,make_scorer,mean_squared_error
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn import datasets , linear_model
from sklearn import svm
from matplotlib import pyplot as plt
from sklearn import metrics
import pandas as pd
import sklearn
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

mysql_info=['root','123456','101.132.126.194','3306','house_price']
database=db.Mysql(mysql_info)
data=database.getdata('preproed_data')
data.drop('id',1,inplace=True)
feature_names=['huxing','mianji','quyu','louceng','chaoxiang','shijian']
target=np.array(data['jiage'])
sh_hp=dict(data=np.array(data),feature_names=np.array(['huxing','mianji','quyu','louceng','chaoxiang','shijian','jiage']),target=np.array(data['jiage']))
features=data.drop('jiage',1)
prices = data['jiage']


# 决定系数计算
def performance_metric(y_true, y_predict):
    score = r2_score(y_true, y_predict)
    return score


# 训练最优模型
def fit_model(X, y):
    cross_validator = KFold(n_splits=10, random_state=1, shuffle=True)
    regressor = DecisionTreeRegressor()
    params = {'max_depth': range(1, 11)}
    scoring_fnc = make_scorer(performance_metric)
    grid = GridSearchCV(regressor, params, scoring=scoring_fnc, cv=cross_validator)
    # 基于输入数据 [X,y]，进行网格搜索
    grid = grid.fit(X, y)
    # 返回网格搜索后的最优模型
    return grid.best_estimator_
'''sh = pd.DataFrame(sh_hp['data'])
sh.columns = sh_hp['feature_names']
sh['danjia'] = sh_hp['target']'''
#模型构建
X = data[['huxing','quyu','mianji','louceng','chaoxiang','shijian']]#
y = data[['jiage']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)#划分训练集测试集
linreg = LinearRegression()#线性回归模型
#linreg.fit(X_train,y_train)
#y_pred = linreg.predict(X_test)
predicted = cross_val_predict(linreg, X, y, cv=10)#十折交叉验证
r2 = performance_metric(y, predicted)
print("线性回归模型RMSE:",np.sqrt(metrics.mean_squared_error(y, predicted)))# 用scikit-learn计算RMSE
print("此数据中线性回归模型的决定系数R^2为{:,.2f}\n".format(r2))
fig, ax = plt.subplots()
ax.scatter(y, predicted)
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()


optimal_reg = fit_model(X_train, y_train)#决策树算法
predicted_price = optimal_reg.predict(X_test)
r2 = performance_metric(y_test, predicted_price)
print("均方根误差RMSE:",np.sqrt(metrics.mean_squared_error(y_test, predicted_price)))
print("此数据中决策回归树模型的决定系数R^2为{:,.2f}".format(r2))# 计算相对于目标变量的决定系数 R2的值
print("最优决策树模型最大深度为{}".format(optimal_reg.get_params()['max_depth']))# 输出最优模型的 'max_depth' 参数
fig, ax = plt.subplots()
ax.scatter(y_test, predicted_price)
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()


'''LR = linear_model.LinearRegression()#最小二乘回归
LR.fit(X_train,y_train)
print('intercept_:%.3f' % LR.intercept_)
#print('coef_:%.3f' % LR.coef_)
print('Mean squared error: %.3f' % mean_squared_error(y_test,LR.predict(X_test)))##((y_test-LR.predict(X_test))**2).mean()
print('Variance score: %.3f' % r2_score(y_test,LR.predict(X_test)))#1-((y_test-LR.predict(X_test))**2).sum()/((y_test - y_test.mean())**2).sum()
print('score: %.3f' % LR.score(X_test,y_test))
plt.plot(X_test ,LR.predict(X_test) ,color='red',linewidth =3)
plt.show()'''

'''clf = svm.SVR()
clf.fit(X_train,y_train)
print('intercept_:%.3f' % clf.intercept_)
print('Mean squared error: %.3f' % mean_squared_error(y_test,clf.predict(X_test)))##((y_test-LR.predict(X_test))**2).mean()
print('Variance score: %.3f' % r2_score(y_test,clf.predict(X_test)))#1-((y_test-LR.predict(X_test))**2).sum()/((y_test - y_test.mean())**2).sum()
print('score: %.3f' % clf.score(X_test,y_test))
plt.plot(X_test ,clf.predict(X_test) ,color='red')
plt.show()'''

'''X = data[['shijian']].values#非线性回归
y = data['danjia'].values
regr = LinearRegression()
# create quadratic features
quadratic = sklearn.preprocessing.PolynomialFeatures(degree=2)
cubic = sklearn.preprocessing.PolynomialFeatures(degree=3)
X_quad = quadratic.fit_transform(X)
X_cubic = cubic.fit_transform(X)
# fit features
X_fit = np.arange(X.min(), X.max(), 1)[:, np.newaxis]

regr = regr.fit(X, y)  # X,y训练数据集建模；X_fit测试数据集预测；对训练数据集测试得分(因为有时根本不知道测试数据集对应的真实y值)
y_lin_fit = regr.predict(X_fit)
linear_r2 = r2_score(y, regr.predict(X))

regr = regr.fit(X_quad, y)
y_quad_fit = regr.predict(quadratic.fit_transform(X_fit))
quadratic_r2 = r2_score(y, regr.predict(X_quad))

regr = regr.fit(X_cubic, y)
y_cubic_fit = regr.predict(cubic.fit_transform(X_fit))
cubic_r2 = r2_score(y, regr.predict(X_cubic))

# plot results
plt.scatter(X, y, label='training points', color='lightgray')
plt.plot(X_fit, y_lin_fit, label='linear (d=1), $R^2=%.2f$' % linear_r2, color='blue', lw=2, linestyle=':')
plt.plot(X_fit, y_quad_fit, label='quadratic (d=2), $R^2=%.2f$' % quadratic_r2, color='red', lw=2, linestyle='-')
plt.plot(X_fit, y_cubic_fit, label='cubic (d=3), $R^2=%.2f$' % cubic_r2, color='green', lw=2, linestyle='--')
plt.xlabel('% lower status of the population [LSTAT]')
plt.ylabel('Price in $1000\'s [MEDV]')
plt.legend(loc='upper right')
plt.tight_layout()
# plt.savefig('./figures/polyhouse_example.png', dpi=300)
plt.show()'''