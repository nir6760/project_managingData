from db_sqlalchemy.db_admin_functions import is_a_admin_poll
from exception_types import DBException, UseException
from db_sqlalchemy.manytomany.db_server import myApp
from sqlalchemy import exc

## ************************************poll functions **********************************************
# check if admin exists
def is_a_poll(id_poll):
    result = False
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
def insert_only_poll(poll_content):
    "fd".endswith("?")
    if not poll_content.endswith("?"):
        poll_content += "?"
    my_app_instance = myApp()
    Poll = my_app_instance.Poll_class
    session = my_app_instance.connDBParams_obj.session_factory()
    id_poll = None
    try:
        new_poll = Poll(poll_content)
        session.add(new_poll)
        session.commit()
        id_poll = new_poll.id_poll  # id_poll is the autoincremented primary_key column. Should work after commit
        poll_content = new_poll.poll_content
        print("Poll was inserted")
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()
        return id_poll, poll_content


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



# insert a new poll with choices to Poll db and Choice db
def insert_poll(poll_content, numbers_choices_dict):
    minimum_allowed_choices = 2
    # check for unique values
    id_poll = None
    flag = len(numbers_choices_dict) != len(set(numbers_choices_dict.values()))
    flag_min = len(set(numbers_choices_dict.values())) < minimum_allowed_choices
    if flag or flag_min:
        raise UseException
    try:
        id_poll, poll_content = insert_only_poll(poll_content)
        if id_poll is not None:
            for key_num, value_answer in numbers_choices_dict.items():
                print(key_num, '->', value_answer)
                insert_only_one_choice(id_poll, key_num, value_answer)
        else:
            raise DBException
    except DBException:
        raise DBException
    except Exception as e:
        print(e)
        raise e
    return id_poll, poll_content


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


# delete poll from Polls db
def delete_poll_by_admin(token, id_poll):
    count_rows = 0
    try:
        is_admin_poll = is_a_admin_poll(token, id_poll)
        if is_admin_poll:
            count_rows = delete_poll(id_poll)
            print("A total of %s rows were deleted." % count_rows)
            # should delete all choices and user_answers because the Foreign Key constraint- delete cascade

        # count_rows = del_ext.rowcount
        # print(count_rows, "users was deleted")
    except DBException:
        raise DBException
    except Exception as e:
        print("An error as occurred, No rows were deleted")
        raise e
    return count_rows


## ************************************polls_telegram functions **********************************************
# check if poll_telegram exists
def is_a_poll_telegram(id_poll, poll_id_telegram):
    result = False
    my_app_instance = myApp()
    PollTelegram = my_app_instance.PollTelegram_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        poll_telegram = PollTelegram.query.filter_by(id_poll=id_poll, poll_id_telegram=poll_id_telegram).first()
        if poll_telegram:
            print("poll_telegram exists: ", id_poll, " : ", poll_id_telegram)
            result = True
        else:
            print("no poll_telegram with this details")
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


# insert a new poll_telegram to PollTelegram db
def insert_poll_telegram(id_poll, poll_id_telegram):
    my_app_instance = myApp()
    PollTelegram = my_app_instance.PollTelegram_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        new_poll_telegram = PollTelegram(id_poll, poll_id_telegram)
        session.add(new_poll_telegram)
        session.commit()
        print("PollTelegram was inserted")
    except exc.IntegrityError as e:
        print(e)
        raise DBException
    except Exception as e:
        print(e)
        raise e
    finally:
        session.close()


# delete poll_telegram from PollTelegram db
def delete_poll_telegram(id_poll, poll_id_telegram):
    my_app_instance = myApp()
    PollTelegram = my_app_instance.PollTelegram_class
    session = my_app_instance.connDBParams_obj.session_factory()
    count_rows = 0
    try:
        del_ext = session.query(PollTelegram).filter(PollTelegram.id_poll == id_poll, PollTelegram.poll_id_telegram == poll_id_telegram)
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


# create list from list query of associates poll_id_telegram
def create_associates_polls_id_telegram_lst(list_query):
    res_lst = []
    for row in list_query:
        res_lst.append(row.poll_id_telegram)
    return res_lst


# get associates poll_id_telegram to specific poll
def getAssociatesPollsIdsTelegramToPoll(id_poll):
    result = (False, None)
    my_app_instance = myApp()
    PollTelegram = my_app_instance.PollTelegram_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(PollTelegram).filter(PollTelegram.id_poll == id_poll).all()
        if len(list_query) != 0:  # An empty result evaluates to False.
            associates_polls_lst = create_associates_polls_id_telegram_lst(list_query)
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

# get id_poll for specific poll_id_telegram
def getIdPollByPollIdTelegram(poll_id_telegram):
    result = (False, None)
    my_app_instance = myApp()
    PollTelegram = my_app_instance.PollTelegram_class
    session = my_app_instance.connDBParams_obj.session_factory()
    try:
        list_query = session.query(PollTelegram).filter(PollTelegram.poll_id_telegram == poll_id_telegram).all()

        if len(list_query) != 0:  # An empty result evaluates to False.
            id_poll = list_query[0].id_poll
            result = (True, id_poll)
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
