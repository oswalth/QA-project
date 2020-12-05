from orm.client import OrmConnector
from orm.models import QaTable


class OrmBuilder:
    def __init__(self, mysql: OrmConnector):
        self.mysql = mysql
        self.engine = self.mysql.connection.engine
        self.table = QaTable

    def get_by_username(self, username):
        return self.mysql.session.query(self.table).filter_by(username=username).first()

    def get_by_email(self, email):
        return self.mysql.session.query(self.table).filter_by(email=email).first()
