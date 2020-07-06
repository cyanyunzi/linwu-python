import pymysql


class DB:
    # 建立连接
    def __init__(self, host='localhost', port=3306, db='', user='root', passwd='root', charset='utf8'):
        print("初始化数据库信息...")
        self.con = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        self.cursor = self.con.cursor()

    # 返回游标
    def __enter__(self):
        return self.cursor

    # 事务处理
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.con.commit()
            print("提交事务...")
        except:
            self.con.rollback()
            print("回滚事务...")
        finally:
            self.con.close()
            print("关闭数据库连接...")
