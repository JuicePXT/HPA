from Data_processing import db,data_pr

mysql_info=['root','123456','localhost','3306','house_price']
mysql=db.Mysql(mysql_info)

raw_data=mysql.getdata('raw_data')
print(raw_data)