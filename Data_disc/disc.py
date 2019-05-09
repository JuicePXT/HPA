"""实现数据离散化的类"""
from pandas import *
from sqlalchemy import create_engine


def readconf(conn, conf_tabname):
    """读取配置表,返回配置列表"""
    rows = read_sql('select * from ' + conf_tabname, conn)
    rows_list = []
    for i in range(0, len(rows)):
        j = rows.loc[i]
        rows_list.append(list(j))
    return rows_list

def conndb(db_info=[]): #username, password, host, port,dbname
    """连接数据库"""
    conn = create_engine('mysql+pymysql://'
                         + db_info[0] + ':' + db_info[1] + '@' + db_info[2] + ':' + db_info[3] +
                         '/' + db_info[4] + '?charset=utf8')  # 连接数据库
    return conn
class Discdata():
    """实现数据离散化,属性有库名，表名，字段名，分段数"""

    def __init__(self,conf=[]):
        """配置列表有0库名，1表名，2字段名，3分段数"""
        self.conf=conf

    def getdata(self,conn):
        """从数据库获取数据"""
        sql1 = 'select ' + self.conf[2] + ' from ' + self.conf[1]#sql语句
        data = read_sql(sql1,conn)#获取数据'
        data=list(data[self.conf[2]])
        return data

    def disdata(self,data):
        """数据离散化，输出分类表，离散边界位标"""
        lable = []
        for i in range(0,self.conf[3]): #创建分段标签
            lable.append(i)
        #data1 = DataFrame({'data': data1})
        disc = cut(data, self.conf[3],labels=lable, retbins=True)  # 分割
        #lab=DataFrame({'level':disc[0]})#总体类别标签
        flag = disc[1]  # 离散边界位标
        #markdf=concat([data1, lab], axis=1)# 原数据和离散标签合并 得到一个DF
        return flag,lable

    def make_boundf(self,flag,lable):
        """生成离散边界表"""
        flag=list(flag)
        min=[]
        max=[]
        dbname=[]
        tabname=[]
        sname=[]
        for i in range(0,self.conf[3]):
            dbname.append(self.conf[0])
            tabname.append(self.conf[1])
            sname.append(self.conf[2])
        min.extend(flag[:-1])
        max.extend(flag[1:])
        dir_dis={'dbname':dbname,'tablename':tabname,'strname':sname,
                 'lable':lable,'min':min,'max':max}
        boundf=DataFrame(dir_dis)
        return boundf

    def store_df(self,dataframe,conn):
        """将表存入数据库,表若存在则追加"""
        tabname= 'distab'
        pandas.io.sql.to_sql(dataframe, tabname, conn, if_exists='append', index=False,
                             chunksize = 10000) #考虑服务器性能将数据拆分成chunksize大小的数据块进行批量插入