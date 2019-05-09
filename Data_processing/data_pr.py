import numpy as np
import pandas as pd
import copy as cp
from matplotlib import pyplot

class Explo():

    def __init__(self,df,str):
        self.df=df
        self.str=str
        self.odf=cp.deepcopy(df)
        self.data=df[str]

    @property
    def sta(self):
        """输出基本统计量df"""
        statistics = self.data.describe()  # 保存基本统计量
        statistics.loc['range'] = statistics.loc['max'] - statistics.loc['min']  # 极差
        statistics.loc['var'] = statistics.loc['std'] / statistics.loc['mean']  # 变异系数
        statistics.loc['dis'] = statistics.loc['75%'] - statistics.loc['25%']  # 四分位数间距
        statistics.loc['upper']=statistics.loc['75%'] + (statistics.loc['75%'] - statistics.loc['25%']) * 1.5
        statistics.loc['lower']=statistics.loc['25%'] - (statistics.loc['75%'] - statistics.loc['25%']) * 1.5
        return statistics

    def non_analyze(self):
        """缺失值分析"""

    def drawBox(self):
        """绘制箱形图"""
        pyplot.boxplot([self.data], labels=['Data'])
        pyplot.title('Box Plot')
        pyplot.show()

class Process(Explo):

    def __init__(self,df,str):
        super().__init__(df,str)

    def dl_outlier(self, lower=None, upper=None):
        """删除异常值,返回异常值位置"""
        if lower is None:
            lower = self.sta['lower']
        if upper is None:
            upper = self.sta['upper']
        olno=[]
        j=0
        for i in range(len(self.data)):
            if self.data[i] < lower or self.data[i] > upper:
                olno.append(i)
                j+=1
                self.data[i] = np.nan
        return olno

    def rt_ol(self,olno):
        ol = pd.DataFrame()
        for n in olno:
            x = self.odf.loc[n]
            ol = ol.append(x)
        fix=cp.deepcopy(self.df)
        fix.rename(columns={self.str: self.str+'_replaced'}, inplace = True)
        fix=fix[self.str+'_replaced']
        ol=pd.concat([ol, fix], axis=1, join='inner')
        return ol

    def rep_nan(self,way=None,value=None):
        """填充缺失值:
            pad/ffill：用前一个非缺失值去填充该缺失值
            backfill/bfill：用下一个非缺失值填充该缺失值
            None：指定一个值去替换缺失值（缺省默认这种方式）"""
        if way == ('ffill' or 'bfill'):
            self.data.fillna(None, method=way, inplace=True)
        elif way is None:
            self.data.fillna(value, method=None, inplace=True)
        elif way in self.sta:
            self.data.fillna(self.sta[way], method=None, inplace=True)
        else:
            print('way值错误')