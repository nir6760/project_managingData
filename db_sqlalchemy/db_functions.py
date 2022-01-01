# coding=utf-8
from exception_types import DBException
from db_sqlalchemy.manytomany.db_server import myApp
from sqlalchemy import exc

## ************************************users functions **********************************************
# check if user exists
def is_a_user(id_user, user_name):
    my_app_instance = myApp()
    User = my_app_instance.User_class
    Poll = my_app_instance.Poll_class
    session = my_app_instance.connDBParams_obj.session_factory()

    list_query = session.query(User).filter(User.id_user == id_user,  User.user_name == user_name).all()
    session.close()

    if len(list_query) != 0:  # An empty result evaluates to False.
        print("id_user: ", id_user, ":", user_name)
        return True
    else:
        print("no user with this details")
        return False

# insert a new user to Users db
def insert_user(id_user, user_name):
    my_app_instance = myApp()
    User = my_app_instance.User_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        new_user = User(id_user, user_name)
        session.add(new_user)
        session.commit()
        print("User was inserted")
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
    finally:
        session.close()


# delete user from Users db
def delete_user(id_user, user_name):
    my_app_instance = myApp()
    User = my_app_instance.User_class
    session = my_app_instance.connDBParams_obj.session_factory()

    count_rows = 0
    try:

        del_ext = session.query(User).filter(User.id_user == id_user,  User.user_name == user_name)
        count_rows = del_ext.delete(synchronize_session=False)
        session.commit()
        print("A total of %s rows were deleted." % count_rows)

        # count_rows = del_ext.rowcount
        # print(count_rows, "users was deleted")
    except exc.IntegrityError as e:
        raise DBException
    except:
        print("An error as occurred, No rows were deleted")
    finally:
        session.close()

    return count_rows

# select password from specific user
def getUserName(id_user):
    my_app_instance = myApp()
    User = my_app_instance.User_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(User).filter(User.id_user == id_user).all()

        session.close()

        if len(list_query) != 0:  # An empty result evaluates to False.
            user_name = list_query[0].user_name
            return True, user_name
        else:
            return False, None

    except exc.IntegrityError as e:
        raise DBException



