from Data_processing import db,data_pr

mysql_info=['root','pantian','localhost','3306','test']
#impala_info=['host','port']
impala_info=['root','pantian','localhost','3306']
mysql=db.Mysql(mysql_info)
confs=db.readconf(mysql.conndb,'conf_tab')#读取配置表
'''配置表：0库名1表名2主键3字段名4上限5下限6空值填充&异常值替换方式(way=None/ffill/bfill/...指定值填充/前一个非缺失值填充/下一个非缺失值填充/统计量填充)
        7填充值（特值填充时）'''
for conf in confs:
    impala_info.append(conf[0])
    impala=db.Mysql(impala_info)
    df=impala.getdata(conf[1],'%s,%s'%(conf[2],conf[3]))#获取数据表，主键+数据
    newpr=data_pr.Process(df,conf[3])#数据处理类
    #newpr.drawBox()
    orgsta=newpr.sta#原始数据统计量
    olno=newpr.dl_outlier() #删除异常值，得到异常值位置列表
    newpr.rep_nan(conf[6],conf[7])
    #缺失值填充(way=None/ffill/bfill/指定值填充/前一个非缺失值填充/下一个非缺失值填充)
    ol=newpr.rt_ol(olno)
    mysql.store_df(ol,conf[3]+'_outliers')#存入数据库
    print('结束')