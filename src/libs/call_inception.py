'''

INCEPTION operation

2017-11-23

cookie

'''

from libs import util
import pymysql
import sqlparse
import ast

pymysql.install_as_MySQLdb()


class Inception(object):
    def __init__(self, LoginDic=None):
        self.__dict__.update(LoginDic)
        self.con = object

    def __enter__(self):
        un_init = util.init_conf()
        inception = ast.literal_eval(un_init['inception'])
        self.con = pymysql.connect(host=inception['host'],
                                   user=inception['user'],
                                   passwd=inception['password'],
                                   port=int(inception['port']),
                                   db='',
                                   charset="utf8")
        return self

    def GenerateStatements(self, Sql: str = '', Type: str = '', backup=None):
        '''
        把通过ssh连接数据库的端口给inception,连接本地数据库密码写死的
        ALTER TABLE `core_databaselist` ADD COLUMN `sshport` int(11) NULL AFTER `after`;
        '''
        get_sshport=pymysql.connect(host='127.0.0.1',user='root',passwd='bbotte',db='yearning',charset='utf8mb4',port=3306,connect_timeout=1)
        sshportcursor = get_sshport.cursor()
        sshportsql = "select sshport from yearning.core_databaselist WHERE ip='{}'".format(self.__dict__.get('host'))
        sshportcursor.execute(sshportsql)
        sshport = sshportcursor.fetchone()[0]
        get_sshport.close()

        if Sql[-1] == ';':
            Sql = Sql.rstrip(';')
        elif Sql[-1] == '；':
            Sql = Sql.rstrip('；')
        if backup is not None and backup != 0:
            InceptionSQL = '''
             /*--user=%s;--password=%s;--host=127.0.0.1;--port=%s;%s;%s;*/ \
             inception_magic_start;\
             use `%s`;\
             %s; \
             inception_magic_commit;
            ''' % (self.__dict__.get('user'),
                   self.__dict__.get('password'),
                   sshport,
                   Type,
                   backup,
                   self.__dict__.get('db'),
                   Sql)
            return InceptionSQL
        else:
            InceptionSQL = '''
                        /*--user=%s;--password=%s;--host=127.0.0.1;--port=%s;%s;*/ \
                        inception_magic_start;\
                        use `%s`;\
                        %s; \
                        inception_magic_commit;
                       ''' % (self.__dict__.get('user'),
                              self.__dict__.get('password'),
                              sshport,
                              Type,
                              self.__dict__.get('db'),
                              Sql)
            return InceptionSQL

    def Execute(self, sql, backup: int):
        if backup == 1:
            Inceptionsql = self.GenerateStatements(Sql=sql, Type='--enable-execute')
        else:
            Inceptionsql = self.GenerateStatements(
                Sql=sql,
                Type='--enable-execute',
                backup='--disable-remote-backup')
        with self.con.cursor() as cursor:
            cursor.execute(Inceptionsql)
            result = cursor.fetchall()
            Dataset = [
                {
                    'ID': row[0],
                    'stage': row[1],
                    'errlevel': row[2],
                    'stagestatus': row[3],
                    'errormessage': row[4],
                    'sql': row[5],
                    'affected_rows': row[6],
                    'sequence': row[7],
                    'backup_dbname': row[8],
                    'execute_time': row[9],
                    'SQLSHA1': row[10]
                }
                for row in result
            ]
        return Dataset

    def Check(self, sql=None):
        Inceptionsql = self.GenerateStatements(Sql=sql, Type='--enable-check')
        with self.con.cursor() as cursor:
            cursor.execute(Inceptionsql)
            result = cursor.fetchall()
            Dataset = [
                {
                    'ID': row[0],
                    'stage': row[1],
                    'errlevel': row[2],
                    'stagestatus': row[3],
                    'errormessage': row[4],
                    'sql': row[5],
                    'affected_rows': row[6],
                    'SQLSHA1': row[10]
                }
                for row in result
            ]
        return Dataset

    def oscstep(self, sql=None):
        with self.con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
        return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    @staticmethod
    def BeautifySQL(sql):
        return sqlparse.format(sql, reindent=True, keyword_case='upper')

    def __str__(self):
        return '''

        InceptionSQL Class

        '''
