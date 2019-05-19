import numpy as np
import pandas as pd
import copy as cp
import sklearn as sk
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

    def mo(self):
        """众数统计"""
        m=self.data.mode()[0]
        return m

    def non_analyze(self):
        """缺失值分析"""
        non_count=self.data.isna().sum()
        print('%s数据有%d个缺失值'%(self.str,non_count))

    def only(self):
        """统计字段数据，不重复地输出字段的值"""
        nore=self.data.drop_duplicates(keep= 'last')
        return nore

    def drawhist(self,bins=None):
        """绘制直方图"""
        pyplot.hist([self.data],bins)
        pyplot.show()

    def drawpie(self):
        """绘制饼图"""
        pyplot.pie([self.data])
        pyplot.show()

    def drawBox(self):
        """绘制箱形图"""
        pyplot.boxplot([self.data])
        pyplot.title('Box Plot')
        pyplot.show()

    def drawcp(self,other):
        """绘制对比图"""
        self.df.plot_trisurf(self.str,other,'scatter')
        pyplot.show()

class Process(Explo):

    def __init__(self,df,str):
        super().__init__(df,str)

    def rep(self,a,b):
        """替换数据值"""
        self.data.replace(a, b,inplace=True)

    def dl_row(self,v):
        """删除包含值v的一行记录"""
        for index, row in self.df.iterrows():
            if v == row[self.str]:
                self.df.drop(index, axis=0, inplace=True)

    def dl_outlier(self, lower=None, upper=None):
        """删除超过箱线图上界的异常值,返回异常值位置序号"""
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
        """输入异常值序号，返回异常值表"""
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
            mode:众数/高频值填充
            None：指定一个值去替换缺失值（缺省默认这种方式）"""
        if way == ('ffill' or 'bfill'):
            self.data.fillna(None, method=way, inplace=True)
        elif way is None:
            self.data.fillna(value, method=None, inplace=True)
        elif way is 'mode':
            self.data.fillna(self.mo(), method=None, inplace=True)
        elif way in self.sta:
            self.data.fillna(self.sta[way], method=None, inplace=True)
        else:
            print('way值错误')