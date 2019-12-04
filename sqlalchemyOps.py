#coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class QueryConn:
    #模仿sqlalchemy的api
    def __init__(self, host='localhost', port='3306', user='root', password='a', db='mysql', charset='UTF8MB4'):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.db=db #数据库名字
        self.charset=charset
        db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset={}'.format(
                    user,
                    password,
                    host,
                    port,
                    db,
                    charset,
                )
        self.db_url=db_url

        engine=create_engine(db_url)
        self.engine=engine
        
        Base = declarative_base(engine)
        self.Base=Base
        
        Session = sessionmaker(engine)
        self.Session=Session
        self.session=Session()

    def connect(self):
        self.connection=self.engine.connect()
        return self.connection
    
    def execute(self,queryString):
        return self.connection.execute('')

if __name__ == '__main__':
    q=QueryConn()
    connection = q.connect()
    result = connection.execute('SELECT * FROM `mysql`.`user` LIMIT 0, 1000')
    print(result.fetchone())
