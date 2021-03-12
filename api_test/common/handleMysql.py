import pymysql
import traceback
import pymssql
from api_automation_test.settings import *
host = DATABASES['default']['HOST']
user = DATABASES['default']['USER']
passwd = DATABASES['default']['PASSWORD']
name = DATABASES['default']['NAME']
def into_sql(sql):#插入数据-mysql
    conn = pymysql.connect(host=host,port=3306,user=user, passwd=passwd, db=name,charset='utf8')
    cur = conn.cursor()
    result=''
    try:
        # 执行SQL语句
        cur.execute(sql)
        conn.commit()
    except:
        # 发生错误时回滚
        conn.rollback()
        print(traceback.format_exc())
        # 关闭数据库连接
    cur.close()
    conn.close()
    return result
def select_sql(sql):#查询
    conn = pymysql.connect(host=host,port=3306,user=user, passwd=passwd, db=name,charset='utf8')
    cur = conn.cursor()
    try:
        # 执行SQL语句
        cur.execute(sql)
        # 获取所有记录列表
        results = cur.fetchall()
    except:
        print(traceback.format_exc())
        print("Error: unable to fetch data")
    # 关闭数据库连接
    cur.close()
    conn.close()
    return results

