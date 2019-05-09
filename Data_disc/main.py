from task.disc import *

mysql_info=['username','password','host','port','dbname']
impala_info=['username','password','host','port']
mysql_conn=conndb(mysql_info) #建立mysql链接
conf_lists=readconf(mysql_conn,'conf_tablename') #得到配置二元列表
for conf in conf_lists: #遍历配置表：0库名，1表名，2字段名，3分段数
    impala_info.append(conf[0]) #根据配置表添加库名
    impala_conn=conndb(impala_info)#建立impala链接

    new_disc=Discdata(conf)

    data=new_disc.getdata(impala_conn)#获取数据
    flag,lable=new_disc.disdata(data)
    boundf=new_disc.make_boundf(flag,lable)

    new_disc.store_df(boundf,mysql_conn) #存储表,储存到配置表所在库
    impala_info.remove(conf[0])#移除库名