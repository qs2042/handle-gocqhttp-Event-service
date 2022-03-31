import sqlite3

class Utils:
    class Inteser:
        INT = "INT"
        INTEGER = "INTEGER"
        TINYINT = ""
        SMALLINT = "SMALLINT"
        MEDIUMINT = "MEDIUMINT"
        BIGINT = "BIGINT"
        UNSIGNED_BIG_INT = "UNSIGNED BIG INT"
        INT2 = "INT2"
        INT8 = "INT8"
    
    class Text:
        def CHARACTER(n=20):
            return "CHARACTER(%s)" % n
        def VARCHAR(n=255):
            return "VARCHAR(%s)" % n
        def VARYING_CHARACTER(n=255):
            return "VARYING CHARACTER(%s)" % n
        def NCHAR(n=55):
            return "NCHAR(%s)" % n
        def NATIVE_CHARACTER(n=70):
            return "NATIVE CHARACTER(%s)" % n
        def NVARCHAR(n=100):
            return "NVARCHAR(%s)" % n
        TEXT = "TEXT"
        CLOB = "CLOB"

    class NONE:
        BLOB = "BLOB"
        NO_DATATYPE_SPECIFIED = "no datatype specified"
    
    class Real:
        REAL = "REAL"
        DOUBLE = "DOUBLE"
        DOUBLE_PRECISION = "DOUBLE PRECISION"
        FLOAT = "FLOAT"

    class Numeric:
        NUMERIC = "NUMERIC"
        BOOLEAN = "BOOLEAN"
        DATE = "DATE"
        DATETIME = "DATETIME"
        def DECIMAL(a=10,b=5):
            return "DECIMAL(%s,%s)" % (a,b)

    class BOOLEAN:  
        # SQLite 没有单独的 Boolean 存储类 0=false, 1=true
        pass

    class DateAndTime: 
        # SQLite 没有一个单独的用于存储日期和/或时间的存储类，但 SQLite 能够把日期和时间存储为 TEXT、REAL 或 INTEGER 值。
        # TEXT	格式为 "YYYY-MM-DD HH:MM:SS.SSS" 的日期。
        # REAL	从公元前 4714 年 11 月 24 日格林尼治时间的正午开始算起的天数。
        # INTEGER	从 1970-01-01 00:00:00 UTC 算起的秒数。
        pass


class SQL:
    def __init__(self, text:str) -> None:
        self.initialization(text)
    
    def __repr__(self) -> str:
        return self.text
    
    def initialization(self, text:str):
        self.rawTest = text
        self.text = text
    
    def isBeautiful(self):
        if self.text[-1:] != " ":
            self.text += " "
    
    def toUpper(self):
        self.text = self.text.upper()
        return self

    def addPrimaryKey(self):
        if not "create table" in self.text:
            return self
        try:
            # 如果原SQL已有参数
            index = self.text.index("(") + 1
            tmp = self.text
            self.text = tmp[0:index] + "ID INT PRIMARY KEY, " + tmp[index:]
        except:
            # 如果原SQL没有参数
            self.text += "(ID INT PRIMARY KEY)"
        
        return self
    
    def WHERE(self, **kwargs):
        self.isBeautiful()
        string = ""
        for i in kwargs:
            if type(kwargs[i]) == str:
                string += "%s='%s'," % (i, kwargs[i])
                continue
            string += "%s=%s," % (i, kwargs[i])
        self.text += "WHERE %s" % string[:-1]
        return self

    def AND(self, **kwargs):
        self.isBeautiful()
        self.text += "AND %s = %s" % (list(kwargs.keys()), list(kwargs.values()))
        return self

    def OR(self, **kwargs):
        self.isBeautiful()
        self.text += "OR %s = %s" % (list(kwargs.keys()), list(kwargs.values()))
        return self

    def like(self, **kwargs):
        self.isBeautiful()
        self.text += "WHERE %s LIKE %s" % (list(kwargs.keys()), list(kwargs.values()))
        return self
        
    def limit(self, Limt, OFFSET):
        self.isBeautiful()
        self.text += "LIMIT %s OFFSET %s" % (Limt, OFFSET)
        return self

    def orderBy(self, **kwargs):pass
    def groupBy(self, **kwargs):pass


def isKwargsEmpty(func):
    def warpper(*args, **kwargs):
        if len(kwargs) == 0:
            return False
        return func(*args, **kwargs)
    return warpper

def isArgsEmpty(func):
    def warpper(*args, **kwargs):
        if len(args) == 0:
            return False
        return func(*args, **kwargs)
    return warpper



class MySqlite3:
    def __init__(self, databaseName) -> None:
        self.initializationConstructorVariable(databaseName)
        self.getConnect()
    
    # 初始化构造器参数
    def initializationConstructorVariable(self, databaseName:str):
        if databaseName.endswith(".db") or databaseName.endswith(".sqlite3"):
            self.databaseName = databaseName
            return None
        self.databaseName = databaseName + ".sqlite3"
        return None
    
    # 连接数据库(数据库不存在则自动创建数据库)
    def getConnect(self):
        self.connect = sqlite3.connect(self.databaseName)
    
    # 关闭连接
    def close(self):
        self.connect.close()

    def execute(self, sql:SQL):
        cursor = self.connect.cursor()
        cursor.execute(sql.text)
        cursor.close()
        return True

    def fetchall(self, sql:SQL):
        cursor = self.connect.cursor()
        cursor.execute(sql.text)
        result = cursor.fetchall()
        cursor.close()
        return result

    def commit(self):
        self.connect.commit()

    #====================================================
    # Table
    #====================================================
    @isArgsEmpty
    @isKwargsEmpty
    def createTable(self, tableName:str, **kwargs):
        sql = "create table %s" % tableName

        sql += "("
        for i in kwargs:
            sql += "%s %s," % (i, kwargs[i])
        sql = sql[:-1] + ")"
        return SQL(sql)

    def deleteTable(self, tableName:str):
        sql = "DROP TABLE %s" % tableName
        return SQL(sql)

    def updateTableName(self, tableNameOld, tableNameNew):
        sql = "ALTER TABLE %s RENAME TO %s" % (tableNameOld, tableNameNew) 
        return SQL(sql)

    #====================================================
    # Field
    #====================================================
    def query(self, tableName:str, *args):
        sql = "SELECT [queryField] FROM %s" % tableName

        if len(args) == 0:
            sql = sql.replace("[queryField]", "*")
            return SQL(sql)
        
        queryField = ""
        for i in args:
            queryField += "%s," % i
        sql = sql.replace("[queryField]", queryField[:-1])
        return SQL(sql)

    def delete(self, tableName:str):
        sql = "DELETE FROM %s" % tableName
        return SQL(sql)

    @isArgsEmpty
    @isKwargsEmpty
    def insert(self, tableName:str, **kwargs):
        sql = "INSERT INTO %s ([key]) VALUES ([value])" % tableName
        sKey = ""
        sValue = ""
        for i in kwargs:
            sKey += "%s," % i
            if type(kwargs[i]) == str:
                sValue += "'%s'," % kwargs[i]
                continue
            sValue += "%s," % kwargs[i]
        sql = sql.replace("[key]", sKey[:-1]).replace("[value]", sValue[:-1])
        return SQL(sql)
    
    @isArgsEmpty
    @isKwargsEmpty
    def update(self, tableName:str, **kwargs):
        sql = "UPDATE %s SET " % tableName
        for i in kwargs:
            sql += "%s=%s," % (i, kwargs[i])
        return SQL(sql[:-1])


def testCreate(s:MySqlite3):
    sql = s.createTable("user", name=Utils.Text.CHARACTER(), account=Utils.Text.VARCHAR(), password=Utils.Text.VARCHAR())
    sql.addPrimaryKey()
    s.execute(sql)
    s.commit()

def testInsert(s:MySqlite3):
    sql = s.insert("user", name="幼晴", account="admin", password="admin")
    s.execute(sql)
    sql = s.insert("user", name="小晴", account="admin", password="admin")
    s.execute(sql)
    sql = s.insert("user", name="大晴", account="admin", password="admin")
    s.execute(sql)
    s.commit()

def testDelete(s:MySqlite3):
    sql = s.delete("user").WHERE(name="幼晴")
    s.execute(sql)
    s.commit()

def testUpdate(s:MySqlite3):
    sql = s.update("user", account="2042136767", password="123456").WHERE(name="大晴")
    s.execute(sql)
    s.commit()

def testSelect(s:MySqlite3):
    sql = s.query("user").WHERE(rowid=2)
    r = s.fetchall(sql)
    s.commit()
    print(r)

if __name__ == "__main__":
    s = MySqlite3("test")
    
    



'''
1.自动获取数据库中的所有表格
    当连接数据库后将数据库中的所有表格转换为Bean
    class Tables:
        表格名 = {"Field":{"字段":"字段属性"}, "其他属性名":"其他属性"}

2.查询的数据自动转换为Bean, 形成ORM映射
    class Bean:
        K = V
        K = V
2.保存数据时,自动将Bean转换为SQL语句


'''





