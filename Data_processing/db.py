import pandas as pd
import impala as imp
import pymysql as pq
from sqlalchemy import create_engine

def readconf(conn, conf_tabname):
    """读取配置表,返回配置二元列表"""
    confs = pd.read_sql('select * from ' + conf_tabname, conn)
    confs_list = []
    for i in range(0, len(confs)):
        j = confs.loc[i]
        confs_list.append(list(j))
    return confs_list

class DB:
    def __init__(self,conf):
        """数据库操作，信息列表"""
        self.conf=conf
    def getdata(self,tab,col='*',key=None):
        """从数据库获取数据,key指定索引"""
        sql = 'select %s from %s' %(col,tab) #limit 1000测试条件限制读取记录条数
        data = pd.read_sql(sql,self.conndb,index_col=key)#获取数据'
        return data
    def store_df(self,dataframe,tabname='newtab'):
        """将表存入数据库,表若存在则追加"""
        pd.io.sql.to_sql(dataframe, tabname, self.conndb, if_exists='append', index=False,
                             chunksize = 10000) #考虑服务器性能将数据拆分成chunksize大小的数据块进行批量插入

class Mysql(DB):
    def __init__(self,conf=[]):
        super().__init__(conf)
    @property
    def conndb(self): #username, password, host, port,dbname
        """连接数据库"""
        conn = create_engine('mysql+pymysql://'
                             + self.conf[0] + ':' + self.conf[1] + '@' + self.conf[2] + ':' + self.conf[3] +
                             '/' + self.conf[4] + '?charset=utf8')  # 连接数据库
        return conn

class Impala:
    def __init__(self,conf=[]):
        super().__init__(conf)
    @property
    def conndb(self):  #host, port,dbname
        """连接数据库"""
        conn = imp.connect(host=self.conf[0], port=self.conf[1])
        return conn