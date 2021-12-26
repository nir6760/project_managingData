# Import libraries
import os
import psycopg2
from db_utils.config_db import config, get_project_root

from exception_types import DBException


class UserType:
    NOT_A_USER = 0
    AUTHENTICATED_USER = 1
    NOT_AUTHENTICATED_USER = 2
    ADMIN = 3


class UserDB:
    def __init__(self):
        try:
            self.PROJECT_ROOT = get_project_root()
            config_db = 'database.ini'
            params = config(os.path.join(self.PROJECT_ROOT, 'db_utils', config_db))
            self.conn = psycopg2.connect(**params)
            self.conn.set_session(autocommit=True)
            self.cur = self.conn.cursor()

            #self.init_DB() ## run only one time at

        except:
            raise DBException('connection exception')

    # with method need it
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()

    # insert a new user to Users db
    def init_DB(self):
        try:
            file_path = os.path.join(self.PROJECT_ROOT, 'db_utils', 'init.sql')

            # try:
            #     # Read file contents
            #     async with aiofiles.open(file_path, mode='r') as f:
            #         sql_as_string = await f.read()
            # except Exception as e:
            #     print(e)

            with open(file_path, mode='r') as sql_file:
                sql_as_string = sql_file.read()

            self.cur.execute(sql_as_string)

            print("Initialized with SQL Script")
            # self.cur.executescript(sql_as_string)
        except psycopg2.IntegrityError as e:
            raise DBException
        except Exception as e:
            print(e)


    # check if user exists
    def is_a_user(self, id_user, user_name):
        self.cur.execute("SELECT 1 FROM public.\"USERS\" WHERE id_user=%s LIMIT 1;", (id_user,))
        if self.cur.fetchone():  # An empty result evaluates to False.
            print("id_user: ", id_user, ":", user_name)
            return True
        else:
            print("false")
            return False

    # insert a new user to Users db
    def insert_user(self, id_user, user_name):
        try:
            self.cur.execute("INSERT INTO public.\"USERS\"(id_user, user_name) VALUES(%s, %s);", (id_user, user_name))
            # self.cur.execute("INSERT INTO public.\"USERS\"(id_user, user_name) VALUES(?, ?);", (id_user, user_name))
            print("User was inserted")
        except psycopg2.IntegrityError as e:
            print(e)
            raise DBException
        except Exception as e:
            print(e)

    # delete user from Users db
    def delete_user(self, id_user, user_name):
        count_rows = 0
        try:

            del_ext = self.cur.execute("DELETE FROM public.\"USERS\" WHERE id_user=%s AND user_name=%s",
                                       (id_user, user_name))

            count_rows = self.cur.rowcount
            print("A total of %s rows were deleted." % count_rows)

            # count_rows = del_ext.rowcount
            # print(count_rows, "users was deleted")
        except psycopg2.IntegrityError as e:
            raise DBException
        except:
            #self.cur.rollback()
            print("An error as occurred, No rows were deleted")

        return count_rows

    # select password from specific user
    def getUserName(self, id_user):
        try:
            self.cur.execute("SELECT user_name FROM public.\"USERS\" WHERE id_user=%s LIMIT 1;", (id_user,))
            user_name = self.cur.fetchone()
            if user_name:
                return True, user_name
            else:
                return False, None
        except psycopg2.IntegrityError as e:
            raise DBException


# test for connection
def test_db():
    d = UserDB()
    d.init_DB()
    #d.delete_user('1','1')
    d.insert_user('1332261387','nir4')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_db()
