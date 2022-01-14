# coding=utf-8
from db_sqlalchemy.db_user_functions import *
from db_sqlalchemy.db_poll_functions import *
from db_sqlalchemy.db_admin_functions import *

## ************************************ use DB functions **********************************************
# parse idPoll_answer to parts
from exception_types import ParsingException


# parse idPoll_answer to id_poll and answer Num
def parseIdPollAnswer(idPoll_answer):
    try:
        one_idPoll_answer_lst = idPoll_answer.split('_')
        if len(one_idPoll_answer_lst) == 1: # can choose id_poll alone
            return one_idPoll_answer_lst[0], None
        elif len(one_idPoll_answer_lst) == 2:
            return one_idPoll_answer_lst[0], int(one_idPoll_answer_lst[1])
        else:
            raise ParsingException
    except Exception as e:
        raise ParsingException


# Python program to illustrate the intersection
# of two lists using set() and intersection()
def intersectLists(lst1, lst2):
    return list(set(lst1) & set(lst2))


# Python program to illustrate the union
# of two lists using set()
def unionLists(lst1, lst2):
    return list(set(lst1) | set(lst2))


# get chat ids as requested
def getChatIdLstToSend(idPoll_answer_lst):
    # result_chat_id_lst = getAllUsersChatIdsLst()
    result_chat_id_lst = []
    for idPoll_answer in idPoll_answer_lst:
        curr_id_poll, curr_answer_num = parseIdPollAnswer(idPoll_answer)
        if curr_id_poll is not None and curr_answer_num is None:
            continue  # can choose id_poll alone
        if curr_id_poll is None and curr_answer_num is None:
            raise ParsingException  # error while parsing
        curr_chat_id_lst = getChatIdsForAnswerInPoll(curr_id_poll, curr_answer_num)
        result_chat_id_lst = unionLists(result_chat_id_lst, curr_chat_id_lst)
    return result_chat_id_lst


## ************************************test DB functions **********************************************
# drop cascade all tables
def drop_cascade_all():
    my_app_instance = myApp()
    try:
        session = my_app_instance.connDBParams_obj.session_destroy()
        session.close()
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e



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
    PollTelegram = my_app_instance.PollTelegram_class
    count_rows = 0
    try:
        delete_records_from_table(User)
        delete_records_from_table(Poll)
        delete_records_from_table(Admin)
        delete_records_from_table(Choices)
        delete_records_from_table(UserAnswer)
        delete_records_from_table(AdminPoll)
        delete_records_from_table(PollTelegram)
    except Exception as e:
        print("An error as occurred, No rows were deleted")
        raise e
    return count_rows


def test_admins():
    print('************** admins **************')
    insert_admin_and_token("nir", "123456", "nir6760")
    insert_admin("nir6769@gmail.com", "123456")
    print(is_a_admin("nir6760@gmail.com"))
    print(is_a_admin("nir6769@gmail.com"))
    print(is_a_admin_with_password("nir6760@gmail.com", "123456"))
    print(is_a_admin_with_password("nir6769@gmail.com", "123456"))
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
    # delete_user("3", "nir3")
    # delete_user("4", "nir4")
    insert_user("1", "nir1")
    insert_user("2", "nir2")
    print()


def test_polls():
    # test choices as well
    print('************** polls **************')
    numbers_choices_dict0 = {0: "choice0", 1: "choice1", 2: "choice2"}
    numbers_choices_dict1 = {3: "choice3", 4: "choice4"}
    insert_poll("poll1", numbers_choices_dict0)
    print(is_a_poll("3"))
    print(is_a_poll("4"))
    delete_poll("3")
    delete_poll("4")
    insert_poll("poll2?", numbers_choices_dict1)
    insert_poll("poll3", numbers_choices_dict0)
    print(getFullPollData(1))
    print()


def test_users_answers():
    print('************** users_answers **************')
    id_poll1 = 1
    id_poll2 = 2
    id_poll3 = 3

    insert_user_answer(1, id_poll1, 0)
    insert_user_answer(3, id_poll1, 2)
    insert_user_answer(2, id_poll1, 2)
    insert_user_answer(2, id_poll2, 3)
    print(is_a_user_answer("1", id_poll1))
    print(is_a_user_answer("1", id_poll2))
    print(getAnswersForPoll(id_poll1))
    print(getAnswersForPoll(id_poll2))
    # delete_user_answer("1", id_poll1)
    # delete_user_answer("1", id_poll2)
    print()


def test_polls_telegram():
    print('************** polls_telegram **************')
    id_poll1 = 1
    id_poll2 = 2
    id_poll3 = 3
    insert_poll_telegram(id_poll1, "1")
    insert_poll_telegram(id_poll1, "2")
    insert_poll_telegram(id_poll2, "3")

    print(getAssociatesPollsIdsTelegramToPoll(id_poll1))
    print(getAssociatesPollsIdsTelegramToPoll(id_poll2))
    print(getAssociatesPollsIdsTelegramToPoll(id_poll3))
    print('allchatidlst : ', getAllUsersChatIdsLst())
    delete_poll_telegram(id_poll2, "3")
    delete_poll_telegram(id_poll2, "4")
    print()


def test_admins_polls():
    print('************** admins_polls **************')
    id_poll1 = 1
    id_poll2 = 2
    id_poll3 = 3

    insert_admin_poll("nir6760", id_poll1)
    # insert_admin_poll("nir6760", id_poll2)
    insert_admin_poll("nir6760", id_poll3)

    print(getAssociatesAdminsToPoll(id_poll1))
    print(getAssociatesPollsToAdmin("nir6760"))
    print(isPollofAdmin("nir6760", 1))
    print(isPollofAdmin("nir6760", 6))
    # delete_admin("nir6760_1@gmail.com", "1234567")
    # delete_poll("1")
    print()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    drop_cascade_all()
    #delete_all_records()
    ##currently need to be in this order
    test_admins()
    test_users()
    test_polls()
    test_users_answers()

    test_polls_telegram()
    test_admins_polls()
    print('************** utils **************')
    print(getChatIdsForAnswerInPoll(1, 2))
    print(getChatIdsForAnswerInPoll(2, 3))
    # print()
    # print(getAnswersForPollByAdmin("nir6760", 1))
    # print()
    # print(creatHistogramForSpecificPoll("nir6760", 2))
    # print()
    # print(getAdminsList())
    print("*********************************************************")
    print(getChatIdLstToSend(["1_0", "2_3"]))
