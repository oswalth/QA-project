import sqlalchemy
from sqlalchemy.orm import sessionmaker


class OrmConnector:

    def __init__(self, user, password, db_name, host, port):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.charset = 'utf8'
        self.connection = self.get_connection()
        session = sessionmaker(bind=self.connection, autocommit=True)
        self.session = session()

    def get_connection(self):
        engine = sqlalchemy.create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            db=self.db_name
        ), encoding=self.charset)
        return engine.connect()
