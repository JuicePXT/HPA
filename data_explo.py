from Data_processing import db,data_pr
#coding:utf-8
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
#有中文出现的情况，需要u'内容'

mysql_info=['root','123456','101.132.126.194','3306','house_price']
database=db.Mysql(mysql_info)
raw_data=database.getdata('raw_data')
xiaoqu=data_pr.Explo(raw_data,'小区名称')
huxing=data_pr.Explo(raw_data,'户型')
mianji=data_pr.Explo(raw_data,'面积')
quyu=data_pr.Explo(raw_data,'区域')
louceng=data_pr.Explo(raw_data,'楼层')
chaoxiang=data_pr.Explo(raw_data,'朝向')
jiage=data_pr.Explo(raw_data,'价格（W）')
danjia=data_pr.Explo(raw_data,'单价（平方米）')
shijian=data_pr.Explo(raw_data,'建筑时间')

#数据缺失值分析
'''xiaoqu.non_analyze()
huxing.non_analyze()
mianji.non_analyze()
quyu.non_analyze()
louceng.non_analyze()
chaoxiang.non_analyze()
jiage.non_analyze()
danjia.non_analyze()
shijian.non_analyze()'''

#字符数据异常值分析
'''print(
    xiaoqu.only(),'\n',
    huxing.only(),'\n',
    quyu.only(),'\n',
    louceng.only(),'\n',
    chaoxiang.only(),'\n',
    shijian.only()
    #字符数据统计
)'''

#数值数据异常值分析
'''mianji.drawBox()
jiage.drawBox()
danjia.drawBox()
print(mianji.sta,jiage.sta,danjia.sta)'''

#数据特征分析

#定性数据分布分析
'''huxing.drawhist()
quyu.drawhist()
louceng.drawhist()
chaoxiang.drawpie()'''

#定量数据分布分析
'''mianji.drawhist(100)
jiage.drawhist(1000)
danjia.drawhist(10000)'''

#对比分析
'''danjia.drawcp('面积')
jiage.drawcp('面积')
danjia.drawcp('价格（W）')'''