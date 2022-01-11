# coding=utf-8
from exception_types import DBException, UseException
from db_sqlalchemy.manytomany.db_server import myApp
from sqlalchemy import exc


## ************************************admin functions **********************************************
# check if admin exists
def is_a_admin(admin_name):
    result = False
    my_app_instance = myApp()
    Admin = my_app_instance.Admin_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        admin = Admin.query.filter_by(admin_name=admin_name).first()
        if admin:
            print("admin_name: ", admin_name)
            result = True
        else:
            print("no admin with this details")
            result = False
        session.close()
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return result


# check if admin - token
def is_a_admin_token(token):
    result = False
    my_app_instance = myApp()
    Admin = my_app_instance.Admin_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        admin = Admin.query.filter_by(token=token).first()
        if admin:
            print("admin_token: ", token)
            result = True
        else:
            print("no admin with this details")
            result = False
        session.close()
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return result


# check if admin with password exists
def is_a_admin_with_password(admin_name, password):
    result = False
    my_app_instance = myApp()
    Admin = my_app_instance.Admin_class
    session = my_app_instance.connDBParams_obj.session_factory()
    print(admin_name, password)
    try:
        admin = Admin.query.filter_by(admin_name=admin_name).first()
        if admin and admin.verify_password(password):
            print("admin_name: ", admin_name, ":", password)
            result = True
        else:
            print("no admin with this details")
            result = False
        session.close()
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return result


# insert a new admin to Admins db
def insert_admin(admin_name, password):
    my_app_instance = myApp()
    Admin = my_app_instance.Admin_class
    token = None
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        new_admin = Admin(admin_name, password)
        session.add(new_admin)
        session.commit()
        token = new_admin.token  # id_poll is the autoincremented primary_key column. Should work after commit
        print("Admin was inserted")
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return token


# delete admin from Admins db
def delete_admin(admin_name, password):
    my_app_instance = myApp()
    Admin = my_app_instance.Admin_class
    session = my_app_instance.connDBParams_obj.session_factory()
    count_rows = 0
    try:
        admin = Admin.query.filter_by(admin_name=admin_name).first()
        count_rows = 0
        if admin and admin.verify_password(password):
            del_ext = session.query(Admin).filter(Admin.admin_name == admin_name)
            count_rows = del_ext.delete(synchronize_session=False)
        session.commit()
        print("A total of %s rows were deleted." % count_rows)

        # count_rows = del_ext.rowcount
        # print(count_rows, "users was deleted")
    except exc.IntegrityError as e:
        raise DBException
    except Exception as e:
        print("An error as occurred, No rows were deleted")
        raise e
    finally:
        session.close()
    return count_rows


# # get admin_name specific admin
# def getAdminName(email_admin):
#     result = (False, None)
#     my_app_instance = myApp()
#     Admin = my_app_instance.Admin_class
#     session = my_app_instance.connDBParams_obj.session_factory()
#     try:
#         list_query = session.query(Admin).filter(Admin.email_admin == email_admin).all()
#
#         if len(list_query) != 0:  # An empty result evaluates to False.
#             admin_name = list_query[0].admin_name
#             result = (True, admin_name)
#         else:
#             result = (False, None)
#
#     except exc.IntegrityError as e:
#         raise DBException
#     except Exception as e:
#         print(e)
#         raise e
#     finally:
#         session.close()
#     return result


# get admin_name specific admin
def getAdminNameByToken(token):
    result = (False, None)
    my_app_instance = myApp()
    Admin = my_app_instance.Admin_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(Admin).filter(Admin.token == token).all()

        if len(list_query) != 0:  # An empty result evaluates to False.
            admin_name = list_query[0].admin_name
            result = (True, admin_name)
        else:
            result = (False, None)

    except exc.IntegrityError as e:
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return result

# get token by specific admin details
def getTokenAndNameByAdminNamePassword(admin_name, password):
    result = (False, (None, None))
    my_app_instance = myApp()
    Admin = my_app_instance.Admin_class
    session = my_app_instance.connDBParams_obj.session_factory()

    try:
        admin = Admin.query.filter_by(admin_name=admin_name).first()
        if admin and admin.verify_password(password):
            list_query = session.query(Admin).filter(Admin.admin_name == admin_name).all()
            if len(list_query) != 0:  # An empty result evaluates to False.
                admin_name = list_query[0].admin_name
                token = list_query[0].token
                result = (True, (token, admin_name))
            else:
                result = (False, (None, None))
        else:
            print("no admin with this details")
            result = False
        session.close()
    except exc.IntegrityError as e:
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return result


## ************************************admins_polls functions **********************************************
# check if admin_poll exists
def is_a_admin_poll(token, id_poll):
    result = False
    my_app_instance = myApp()
    AdminPoll = my_app_instance.AdminPoll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        if is_a_admin_token(token):  # get this only if the real admin asked
            admin_poll = AdminPoll.query.filter_by(token=token, id_poll=id_poll).first()
            if admin_poll:
                print("admin_poll exists: ", 'token : ', token, " : ", id_poll)
                result = True
            else:
                print("no admin_poll with this details")
                result = False
        session.close()
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return result


# insert a new admin_pol to AdminPoll db
def insert_admin_poll(token, id_poll):
    my_app_instance = myApp()
    AdminPoll = my_app_instance.AdminPoll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        if is_a_admin_token(token):  # insert this only if the real admin asked
            new_admin_poll = AdminPoll(token, id_poll)
            session.add(new_admin_poll)
            session.commit()
            print("AdminPoll was inserted")
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


# delete admin_poll from AdminPoll db
def delete_admin_poll(token, id_poll):
    my_app_instance = myApp()
    AdminPoll = my_app_instance.AdminPoll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    count_rows = 0
    try:
        del_ext = session.query(AdminPoll).filter(AdminPoll.token == token, AdminPoll.id_poll == id_poll)
        count_rows = del_ext.delete(synchronize_session=False)
        session.commit()
        print("A total of %s rows were deleted." % count_rows)
        # count_rows = del_ext.rowcount
        # print(count_rows, "users was deleted")
    except exc.IntegrityError as e:
        raise DBException
    except Exception as e:
        print("An error as occurred, No rows were deleted")
        raise e
    finally:
        session.close()
    return count_rows


# create list from list query of associates polls
def create_associates_polls_lst(list_query):
    res_lst = []
    for row in list_query:
        res_lst.append(row.id_poll)
    return res_lst


# get associates polls to specific admin
def getAssociatesPollsToAdmin(token):
    result = (False, None)
    my_app_instance = myApp()
    AdminPoll = my_app_instance.AdminPoll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(AdminPoll).filter(AdminPoll.token == token).all()

        if len(list_query) != 0:  # An empty result evaluates to False.
            associates_polls_lst = create_associates_polls_lst(list_query)
            result = (True, associates_polls_lst)
        else:
            result = (False, None)

    except exc.IntegrityError as e:
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return result


# # get associates polls to specific admin with password
# def getAssociatesPollsToAdminPassword(email_admin, password):
#     result = (False, None)
#     try:
#         is_admin = is_a_admin_with_password(email_admin, password)
#         if is_admin:
#             result = getAssociatesPollsToAdmin(email_admin)
#     except DBException:
#         raise DBException
#     except Exception as e:
#         print("An error as occurred, No rows were deleted")
#         raise e
#     return result


# create list from list query of associates admins
def create_associates_admins_lst(list_query):
    res_lst = []
    for row in list_query:
        res_lst.append(row.token)
    return res_lst


# get associates admins tokens to specific poll
def getAssociatesAdminsToPoll(id_poll):
    result = (False, None)
    my_app_instance = myApp()
    AdminPoll = my_app_instance.AdminPoll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(AdminPoll).filter(AdminPoll.id_poll == id_poll).all()

        if len(list_query) != 0:  # An empty result evaluates to False.
            associates_admins_lst = create_associates_admins_lst(list_query)
            result = (True, associates_admins_lst)
        else:
            result = (False, None)

    except exc.IntegrityError as e:
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return result
