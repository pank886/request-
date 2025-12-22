from common.recordlog import logs
from conf.operationConfig import OperationConfig

import pymysql

conf = OperationConfig()

class CommectMysql:
    """
    连接读取数据库
    避免sql注入请使用"SELECT * FROM users WHERE name = %s", (name)结构
    """

    def __init__(self):

        mysql_conf = {
            'host': conf.get_MySQL('host'),
            'port': int(conf.get_MySQL('port')),
            'user': conf.get_MySQL('user'),
            'password': conf.get_MySQL('password'),
            'database': conf.get_MySQL('database')
        }
        try:
            self.conn = pymysql.connect(**mysql_conf, charset = 'utf8mb4')
            self.cursor = self.conn.cursor(cursor = pymysql.cursors.DictCursor)
            logs.info("""
                成功连接到Mysql数据库
                host：{host}
                port:{port}
                db:{database}
            """.format(**mysql_conf))
        except Exception as e:
            logs.error(e)

    def close(self):
        """关闭数据库连接"""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
        logs.info("MySQL 连接已关闭")

    def execute_updata(self, sql, data=None):
        """
        执行写操作：增、删、改
        :param sql: sql语句
        :param data: 参数（元组/列表/None）
        :return:
        """
        try:
            if data is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logs.error(f"写操作失败: {e}\nSQL: {sql}\nData: {data}")
        finally:
            self.close()

    def executemany_updata(self, sql, data=None):
        """
        执行多条写操作：增、删、改（仅提升可读性，不增加性能，不要超过500条）
        :param sql: sql语句
        :param data: 插入数据（一般是列表套元组）
        :return:
        """

        if not data:
            logs.warning("executemany_sql 被调用但未提供有效数据，跳过执行。")
            return False

        try:
            self.cursor.executemany(sql, data)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logs.error(f"插入失败: {e}\nSQL: {sql}\nData: {data}")
        finally:
            self.close()

    def query(self, sql, data=None, one=False):
        """
        查询操作
        :param sql: SQL 查询语句（建议使用 %s 占位符）
        :param data: 参数（元组/列表/字典），用于填充占位符
        :param one: 是否只返回第一条结果（True → dict；False → list of dict）
        :return:
            - one=True:  字典（如 {'id': 1, 'name': 'Alice'}）或 None
            - one=False: 列表 of 字典（如 [{'id':1, 'name':'Alice'}, ...]）
        """
        try:
            # 执行查询
            if data is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, data)

            # 获取列名
            columns = [desc[0] for desc in self.cursor.description] if self.cursor.description else []

            if one:
                #查询下一行，没有返回None
                return self.cursor.fetchone()
            else:
                return self.cursor.fetchall()

        except Exception as e:
            logs.error(f"查询失败： {e}\nSQL: {sql}\nParams: {data}")
        finally:
            self.close()