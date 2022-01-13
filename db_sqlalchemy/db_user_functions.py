# coding=utf-8
from db_sqlalchemy.db_utils_func import getChoicesForPoll
from exception_types import DBException, UseException
from db_sqlalchemy.manytomany.db_server import myApp
from sqlalchemy import exc

from db_sqlalchemy.db_admin_functions import is_a_admin_poll, is_a_admin_token


## ************************************users functions **********************************************
# check if user exists
def is_a_user(id_user, user_name):
    result = False
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
    result = (False, None)
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


# get user_name specific user
def getAllUsersChatIdsLst():
    all_chat_ids_lst = []
    my_app_instance = myApp()
    User = my_app_instance.User_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(User).all()
        for row in list_query:
            all_chat_ids_lst.append(row.id_user)
        session.close()
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
    return all_chat_ids_lst


## ************************************users_answers functions **********************************************
# check if user_answer exists for a specific poll
def is_a_user_answer(id_user, id_poll):
    result = False
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
    result = (False, None)
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


# create histogram from answers to specific poll
def creatHistogramForSpecificPoll(token, id_poll):
    answers_hist_dict = {}
    numbers_answers_exists, numbers_answers_dict = getChoicesForPoll(id_poll)
    if numbers_answers_exists:
        for key, value in numbers_answers_dict.items():
            answers_hist_dict[value] = 0
        answers_for_poll_exists, answer_for_poll_dict = getAnswersForPollByAdmin(token, id_poll)
        if answers_for_poll_exists:
            for key, value in answer_for_poll_dict.items():
                poll_content = numbers_answers_dict[value]
                if value in answers_hist_dict:
                    answers_hist_dict[poll_content] += 1
                else:
                    answers_hist_dict[poll_content] = 1

    return answers_hist_dict


# get all answers from specific poll
def getAnswersForPollByAdmin(token, id_poll):
    result = (False, None)
    try:
        is_admin_poll = is_a_admin_poll(token, id_poll)
        if is_admin_poll:
            result = getAnswersForPoll(id_poll)
    except DBException:
        raise DBException
    except Exception as e:
        print("An error as occurred, No rows were deleted")
        raise e
    return result


# get all answers from specific poll
def getChatIdsForAnswerInPollByAdminToken(token, id_poll, answer_number):
    chat_ids_lst = []
    try:
        users_answers_dict_exists, users_answers_dict = getAnswersForPollByAdmin(token, id_poll)
        if users_answers_dict_exists:
            # filter dictionary to contain only users who answered answer_number
            users_answers_new_dict = dict(filter(lambda elem: elem[1] == answer_number, users_answers_dict.items()))
            chat_ids_lst = list(users_answers_new_dict.keys())
    except DBException:
        raise DBException
    except Exception as e:
        print("An error as occurred, No rows were deleted")
        raise e
    return chat_ids_lst

# get all answers from specific poll
def getChatIdsForAnswerInPoll(id_poll, answer_number):
    chat_ids_lst = []
    try:
        users_answers_dict_exists, users_answers_dict = getAnswersForPoll(id_poll)
        if users_answers_dict_exists:
            # filter dictionary to contain only users who answered answer_number
            users_answers_new_dict = dict(filter(lambda elem: elem[1] == answer_number, users_answers_dict.items()))
            chat_ids_lst = list(users_answers_new_dict.keys())
    except DBException:
        raise DBException
    except Exception as e:
        print("An error as occurred, No rows were deleted")
        raise e
    return chat_ids_lst
