#数据清洗
import re
from Data_processing import db,data_pr

mysql_info=['root','123456','101.132.126.194','3306','house_price']
database=db.Mysql(mysql_info)
raw_data=database.getdata('raw_data')
chaoxiang=data_pr.Process(raw_data,'朝向')
quyu=data_pr.Process(raw_data,'区域')
jiage=data_pr.Process(raw_data,'价格（W）')
shijian=data_pr.Process(raw_data,'建筑时间')
mianji=data_pr.Process(raw_data,'面积')
id=data_pr.Process(raw_data,'ID')

#缺失值处理
#print('建筑时间和朝向的众数分别是',shijian.mo(),chaoxiang.mo())
shijian.rep_nan('mode')
chaoxiang.rep_nan('mode')

#异常值处理
cxmode=chaoxiang.mo()
for i in ['朝','(进门)','(进门) 北','(进门) 东','(进门) 东南','(进门) 东西','(进门) 南','(进门) 南北','(进门) 西','(进门) 西北','(进门) 西南']:
    chaoxiang.rep(i,cxmode)
quyu.rep('闸北','静安')#区域异常值处理
out_lier=[2627,20842,23941]#数值异常值记录ID
for i in out_lier:
    id.dl_row(i)

i=0
for row in shijian.df.itertuples():   #将建设时间转换为整型数值
    y=re.findall(r'\d+',row[10])[0]
    raw_data.iloc[i,9]=y
    if re.match(r'地上.*',row[6]): #去掉楼层具体层数
        raw_data.iloc[i, 5]='别墅'
    else:
        raw_data.iloc[i,5]=row[6].split('/')[0]
    if int(y)<1960:         #离散化建筑时间
        raw_data.iloc[i, 9]='旧'
    elif int(y)>=1960 and int(y)<2000:
        raw_data.iloc[i, 9] = '一般'
    else:
        raw_data.iloc[i, 9] = '新'
    raw_data.iloc[i, 7]=row[8]*10000
    i=i+1

database.store_df(shijian.df,'clean_data')
print("数据清洗完成，净数据已导入数据库。")