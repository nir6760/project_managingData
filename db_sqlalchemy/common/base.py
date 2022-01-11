import os

from flask_sqlalchemy import SQLAlchemy
from db_utils.config_db import config_params, get_project_root

from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


class connDBParams():
    def __init__(self, app):
        self.PROJECT_ROOT = get_project_root()
        self.config_db = 'database.ini'
        self.params = config_params()
        self.user_name = self.params['user']
        self.password = self.params['password']
        self.host = self.params['host']
        self.port = self.params['port']
        self.database = self.params['database']
        self.uri = f'postgresql://{self.user_name}:{self.password}@{self.host}:{self.port}/{self.database}'

        app.config["SQLALCHEMY_DATABASE_URI"] = self.uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = SQLAlchemy(app)
        self._SessionFactory = None
        self.Base = self.db.Model


    def session_factory(self):
        self._SessionFactory = self.db.sessionmaker(self.db.engine, autocommit=False, autoflush=False)
        self.db.metadata.create_all(self.db.engine)
        return self._SessionFactory()


    def session_destroy(self):
        self._SessionFactory = self.db.sessionmaker(self.db.engine, autocommit=False, autoflush=False)
        self.db.metadata.drop_all(self.db.engine)
        print('all dropped')

        return self._SessionFactory()
