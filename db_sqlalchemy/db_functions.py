# coding=utf-8
from exception_types import DBException
from db_sqlalchemy.manytomany.db_server import myApp
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash


## ************************************users functions **********************************************
# check if user exists
def is_a_user(id_user, user_name):
    result = None
    my_app_instance = myApp()
    User = my_app_instance.User_class
    session = my_app_instance.connDBParams_obj.session_factory()
    print(id_user, user_name)
    try:
        list_query = session.query(User).filter(User.id_user == id_user, User.user_name == user_name).all()
        session.close()
        if len(list_query) != 0:  # An empty result evaluates to False.
            print("id_user: ", id_user, ":", user_name)
            result = True
        else:
            print("no user with this details")
            result = False
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return result


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
        raise e
    finally:
        session.close()


# delete user from Users db
def delete_user(id_user, user_name):
    my_app_instance = myApp()
    User = my_app_instance.User_class
    session = my_app_instance.connDBParams_obj.session_factory()

    count_rows = 0
    try:

        del_ext = session.query(User).filter(User.id_user == id_user, User.user_name == user_name)
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


# get user_name specific user
def getUserName(id_user):
    result = None
    my_app_instance = myApp()
    User = my_app_instance.User_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(User).filter(User.id_user == id_user).all()

        if len(list_query) != 0:  # An empty result evaluates to False.
            user_name = list_query[0].user_name
            result = (True, user_name)
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


## ************************************users_answers functions **********************************************
# check if user_answer exists for a specific poll
def is_a_user_answer(id_user, id_poll):
    result = None
    my_app_instance = myApp()
    UserAnswer = my_app_instance.UserAnswer_class
    session = my_app_instance.connDBParams_obj.session_factory()
    print(id_user, id_poll)
    try:
        list_query = session.query(UserAnswer).filter(UserAnswer.id_user == id_user,
                                                      UserAnswer.id_poll == id_poll).all()
        session.close()
        if len(list_query) != 0:  # An empty result evaluates to False.
            print("id_user: ", id_user, " - id_poll:", id_poll)
            result = True
        else:
            print("no user_answer with this details")
            result = False
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return result


# insert a new user_answer to UsersAnswers db
def insert_user_answer(id_user, id_poll, number):
    my_app_instance = myApp()
    UserAnswer = my_app_instance.UserAnswer_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        new_user_answer = UserAnswer(id_user, id_poll, number)
        session.add(new_user_answer)
        session.commit()
        print("UserAnswer was inserted")
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


# delete user_answer from UsersAnswers db
def delete_user_answer(id_user, id_poll):
    my_app_instance = myApp()
    UserAnswer = my_app_instance.UserAnswer_class
    session = my_app_instance.connDBParams_obj.session_factory()
    count_rows = 0
    try:

        del_ext = session.query(UserAnswer).filter(UserAnswer.id_user == id_user, UserAnswer.id_poll == id_poll)
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


# create dictionary from list query of users answers
def create_user_answer_dict_with_username(list_query):
    res_dict = {}
    for row in list_query:
        user_name = getUserName(row.id_user)
        res_dict[row.id_user] = (user_name, row.number)
    return res_dict


# create dictionary from list query of users answers
def create_user_answer_dict(list_query):
    res_dict = {}
    for row in list_query:
        res_dict[row.id_user] = row.number
    return res_dict


# get all answers from specific poll
def getAnswersForPoll(id_poll):
    result = None
    my_app_instance = myApp()
    UserAnswer = my_app_instance.UserAnswer_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(UserAnswer).filter(UserAnswer.id_poll == id_poll).all()

        if len(list_query) != 0:  # An empty result evaluates to False.
            users_answers_dict = create_user_answer_dict(list_query)
            print(users_answers_dict)
            result = (True, users_answers_dict)
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


## ************************************admin functions **********************************************
# check if admin exists
def is_a_admin(email_admin, password):
    result = None
    my_app_instance = myApp()
    Admin = my_app_instance.Admin_class
    session = my_app_instance.connDBParams_obj.session_factory()
    print(email_admin, password)
    try:
        admin = Admin.query.filter_by(email_admin=email_admin).first()
        if admin and admin.verify_password(password):
            print("email_admin: ", email_admin, ":", password)
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
def insert_admin(email_admin, password):
    my_app_instance = myApp()
    Admin = my_app_instance.Admin_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        new_admin = Admin(email_admin, password)
        session.add(new_admin)
        session.commit()
        print("Admin was inserted")
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


# delete admin from Admins db
def delete_admin(email_admin, password):
    my_app_instance = myApp()
    Admin = my_app_instance.Admin_class
    session = my_app_instance.connDBParams_obj.session_factory()
    count_rows = 0
    try:
        admin = Admin.query.filter_by(email_admin=email_admin).first()
        count_rows = 0
        if admin and admin.verify_password(password):
            del_ext = session.query(Admin).filter(Admin.email_admin == email_admin)
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


## ************************************poll functions **********************************************
# check if admin exists
def is_a_poll(id_poll):
    result = None
    my_app_instance = myApp()
    Poll = my_app_instance.Poll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    print(id_poll)
    try:
        admin = Poll.query.filter_by(id_poll=id_poll).first()
        if admin:
            print("id_poll exists: ", id_poll)
            result = True
        else:
            print("no poll with this details")
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


# insert a new poll to Poll db
def insert_only_poll(id_poll, poll_content):
    my_app_instance = myApp()
    Poll = my_app_instance.Poll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        new_poll = Poll(id_poll, poll_content)
        session.add(new_poll)
        session.commit()
        print("Poll was inserted")
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


## ************************************choices functions **********************************************
# insert a new choices to Choices db
def insert_only_one_choice(id_poll, number, answer):
    my_app_instance = myApp()
    Choices = my_app_instance.Choice_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        new_choice = Choices(id_poll, number, answer)
        session.add(new_choice)
        session.commit()
        print("Choice was inserted")
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


# create dictionary from list query of choices
def create_numbers_answers_dict(list_query):
    res_dict = {}
    for row in list_query:
        res_dict[row.number] = row.answer
    return res_dict


# get all choices from specific poll
def getChoicesForPoll(id_poll):
    result = None
    my_app_instance = myApp()
    Choices = my_app_instance.Choice_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(Choices).filter(Choices.id_poll == id_poll).all()

        if len(list_query) != 0:  # An empty result evaluates to False.
            numbers_answers_dict = create_numbers_answers_dict(list_query)
            print(numbers_answers_dict)
            result = (True, numbers_answers_dict)
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


# insert a new poll with choices to Poll db and Choice db
def insert_poll(id_poll, q_content, number_choice_dict):
    try:
        insert_only_poll(id_poll, q_content)
    except DBException:
        raise DBException
    except Exception as e:
        print(e)
        raise e
    for key_num, value_answer in number_choice_dict.items():
        print(key_num, '->', value_answer)
        try:
            insert_only_one_choice(id_poll, key_num, value_answer)
        except exc.IntegrityError as e:
            print(e)
            raise DBException
        except Exception as e:
            print(e)
            raise e


# delete poll from Polls db
def delete_poll(id_poll):
    my_app_instance = myApp()
    Poll = my_app_instance.Poll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    count_rows = 0
    try:
        del_ext = session.query(Poll).filter(Poll.id_poll == id_poll)
        count_rows = del_ext.delete(synchronize_session=False)
        session.commit()
        print("A total of %s rows were deleted." % count_rows)
        # should delete all choices and user_answers because the Foreign Key constraint- delete cascade

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


# get q_content and date specific poll
def getPollContentAndDate(id_poll):
    result = None
    my_app_instance = myApp()
    Poll = my_app_instance.Poll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(Poll).filter(Poll.id_poll == id_poll).all()

        if len(list_query) != 0:  # An empty result evaluates to False.
            poll_content = list_query[0].poll_content
            date = list_query[0].date
            result = (True, (poll_content, date))
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


## ************************************admins_polls functions **********************************************
# insert a new user to Users db
def insert_admin_poll(email_admin, id_poll):
    my_app_instance = myApp()
    AdminPoll = my_app_instance.AdminPoll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        new_admin_poll = AdminPoll(email_admin, id_poll)
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


# delete user from Users db
def delete_admin_poll(email_admin, id_poll):
    my_app_instance = myApp()
    AdminPoll = my_app_instance.AdminPoll_class
    session = my_app_instance.connDBParams_obj.session_factory()

    count_rows = 0
    try:

        del_ext = session.query(AdminPoll).filter(AdminPoll.email_admin == email_admin, AdminPoll.id_poll == id_poll)
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


# get user_name specific user
def getAssociatesPollsToAdmin(email_admin):
    result = None
    my_app_instance = myApp()
    AdminPoll = my_app_instance.AdminPoll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(AdminPoll).filter(AdminPoll.email_admin == email_admin).all()

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


# create list from list query of associates admins
def create_associates_admins_lst(list_query):
    res_lst = []
    for row in list_query:
        res_lst.append(row.email_admin)
    return res_lst


# get user_name specific user
def getAssociatesAdminsToPoll(id_poll):
    result = None
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


## ************************************utillis functions **********************************************
# delete records from table
def delete_records_from_table(Model):
    my_app_instance = myApp()
    session = my_app_instance.connDBParams_obj.session_factory()
    count_rows = 0
    try:
        # for all records
        del_ext = session.query(Model)
        count_rows = del_ext.delete(synchronize_session=False)
        session.commit()
        print(f"A total of %s rows were deleted. from {Model.__tablename__}" % count_rows)

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


# delete all records from all the tables
def delete_all_records():
    my_app_instance = myApp()
    User = my_app_instance.User_class
    Poll = my_app_instance.Poll_class
    Admin = my_app_instance.Admin_class
    Choices = my_app_instance.Choice_class
    UserAnswer = my_app_instance.UserAnswer_class
    AdminPoll = my_app_instance.AdminPoll_class
    count_rows = 0
    try:
        delete_records_from_table(User)
        delete_records_from_table(Poll)
        delete_records_from_table(Admin)
        delete_records_from_table(Choices)
        delete_records_from_table(UserAnswer)
        delete_records_from_table(AdminPoll)
    except Exception as e:
        print("An error as occurred, No rows were deleted")
        raise e
    return count_rows


def test_admins():
    print('************** admins **************')
    insert_admin("nir6769@gmail.com", "123456")
    print(is_a_admin("nir6760@gmail.com", "123456"))
    print(is_a_admin("nir6769@gmail.com", "123456"))
    delete_admin("nir6760@gmail.com", "123456")
    delete_admin("nir6769@gmail.com", "123456")
    insert_admin("nir6760_1@gmail.com", "1234567")
    insert_admin("nir6760_2@gmail.com", "1234567")
    print()


def test_users():
    print('************** users **************')
    insert_user("3", "nir3")
    print(is_a_user("3", "nir3"))
    print(is_a_user("4", "nir4"))
    delete_user("3", "nir3")
    delete_user("4", "nir4")
    insert_user("1", "nir1")
    insert_user("2", "nir2")
    print()


def test_polls():
    # test choices as well
    print('************** polls **************')
    number_choice_dict0 = {0: "choice0", 1: "choice1", 2: "choice2"}
    number_choice_dict1 = {3: "choice3", 4: "choice4"}
    insert_poll("3", "poll3", number_choice_dict0)
    print(is_a_poll("3"))
    print(is_a_poll("4"))
    delete_poll("3")
    delete_poll("4")
    insert_poll("1", "poll1", number_choice_dict1)
    insert_poll("2", "poll2", number_choice_dict0)
    print()


def test_users_answers():
    print('************** users_answers **************')
    insert_user_answer("1", "2", 0)
    insert_user_answer("2", "1", 3)
    print(is_a_user_answer("1", "1"))
    print(is_a_user_answer("1", "2"))
    print(getAnswersForPoll("1"))
    print(getAnswersForPoll("2"))
    delete_user_answer("1", "1")
    delete_user_answer("1", "2")
    print()


def test_admins_polls():
    print('************** admins_polls **************')
    insert_admin_poll("nir6760_1@gmail.com", "1")
    insert_admin_poll("nir6760_2@gmail.com", "1")
    insert_admin_poll("nir6760_2@gmail.com", "2")

    print(getAssociatesAdminsToPoll("1"))
    print(getAssociatesPollsToAdmin("nir6760_2@gmail.com"))
    delete_admin("nir6760_1@gmail.com", "1234567")
    print(getAssociatesAdminsToPoll("1"))
    delete_poll("1")
    print()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    delete_all_records()
    # currently need to be in this order
    test_admins()
    test_users()
    test_polls()
    test_users_answers()
    test_admins_polls()
