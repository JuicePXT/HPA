import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from Data_processing import db

mysql_info=['root','123456','101.132.126.194','3306','house_price']
database=db.Mysql(mysql_info)
# 定义空列表，用于创建所有的爬虫链接
urls = []
# 指定爬虫所需的上海各个区域名称
districts = ['pudong', 'minhang', 'baoshan', 'xuhui', 'putuo', 'yangpu', 'changning', 'songjiang',
             'jiading', 'huangpu', 'jinan', 'zhabei', 'hongkou', 'qingpu', 'fengxian', 'jinshan', 'chongming']
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'sh.lianjia.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
}
df = pd.DataFrame(
    columns=('title', 'quyu', 'xiaoqu', 'huxing', 'chaoxiang', 'loucheng', 'zhuangxiu', 'dianti', 'shijian', 'mianji',
             'danjia', 'jiage'))
# 基于for循环，构造完整的爬虫链接
for i in districts:
    '''url = 'https://sh.lianjia.com/ershoufang/%s/' % i
    res = requests.get(url,headers=headers)  # 发送get请求
    res = res.text.encode(res.encoding).decode('utf-8')  # 需要转码，否则会有问题
    soup = BeautifulSoup(res, 'html.parser')  # 使用bs4模块，对响应的链接源代码进行html解析
    page = soup.findAll('div', {'class': 'page-box house-lst-page-box'})  # 使用finalAll方法，获取指定标签和属性下的内容
    pages = [i.strip() for i in page[0].text.split('\n')]  # 抓取出每个区域的二手房链接中所有的页数
    if len(pages) > 3:
        total_pages = int(pages[-3])
    else:
        total_pages = int(pages[-2])'''
    for j in list(range(1, 101)):  # 拼接所有需要爬虫的链接
        urls.append('http://sh.lianjia.com/ershoufang/%s/d%s' % (i, j))

# 创建csv文件，用于后面的保存数据
file = open('lianjia.csv', 'w', encoding='utf-8')

for url in urls:  # 基于for循环，抓取出所有满足条件的标签和属性列表，存放在find_all中
    res = requests.get(url, headers=headers)
    res = res.text.encode(res.encoding).decode('utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    find_all = soup.find_all(name='div', attrs={'class': 'info clear'})

    for i in list(range(len(find_all))):  # 基于for循环，抓取出所需的各个字段信息
        res2 = find_all[i]
        title = res2.find_all('div', {'class': 'title'})[0].text  # 每套二手房的标题
        address = res2.find_all('div', {'class': 'address'})[0].text.split(' | ')  # 每套二手房的小区名称
        xiaoqu = address[0].strip()
        huxing = address[1]
        mianji = address[2]
        chaoxiang = address[3]
        zhuangxiu = address[4]
        dianti = address[5]

        flood = res2.find_all('div', {'class': 'flood'})[0].text
        flood = re.split(r"(....年)", flood)
        loucheng = flood[0]+')'  # 每套二手房所在的楼层
        shijian = flood[1]  # 每套二手房的建筑时间
        quyu = flood[2].split('-')[1].strip()  # 每套二手房所属的区域

        price = res2.find_all('div', {'class': 'priceInfo'})[0].text.split('单价')
        # 每套二手房的总价
        jiage = price[0]
        # 每套二手房的平方米售价
        danjia = price[1]

        # print(name,room_type,size,region,loucheng,chaoxiang,price,price_union,builtdate)
        df.loc[i] = [title, quyu, xiaoqu, huxing, chaoxiang, loucheng, zhuangxiu, dianti, shijian, mianji,
                     danjia, jiage]
        # 将上面的各字段信息值写入并保存到csv文件中
        file.write(','.join((title, quyu, xiaoqu, huxing, chaoxiang, loucheng, zhuangxiu, dianti, shijian, mianji,
                             danjia, jiage)) + '\n')


database.store_df(df,'raw_data_%s'%(str(time.strftime("%Y/%m/%d"))))
# 关闭文件（否则数据不会写入到csv文件中）
file.close()
