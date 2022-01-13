# coding=utf-8
from exception_types import DBException, UseException
from db_sqlalchemy.manytomany.db_server import myApp
from sqlalchemy import exc

# create dictionary from list query of choices
def create_numbers_answers_dict(list_query):
    res_dict = {}
    for row in list_query:
        res_dict[row.number] = row.answer
    return res_dict

# get all choices from specific poll
def getChoicesForPoll(id_poll):
    result = (False, None)
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


# get q_content and date specific poll
def getPollContentAndDate(id_poll):
    result = (False, None)
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


# get poll_content and date and choices to specific poll
def getFullPollData(id_poll):
    result = (False, None)
    my_app_instance = myApp()
    Poll = my_app_instance.Poll_class
    try:
        poll_date_res = getPollContentAndDate(id_poll)
        if poll_date_res[0]:
            poll_content = poll_date_res[1][0]
            date = poll_date_res[1][1]
            numbers_answers = getChoicesForPoll(id_poll)
            if numbers_answers[0]:
                numbers_answers_dict = numbers_answers[1]
                res_dict = {
                    'poll_content': poll_content,
                    'date': date,
                    'numbers_answers_dict': numbers_answers_dict
                }
                result = (True, res_dict)
    except DBException:
        raise DBException
    except Exception as e:
        print(e)
        raise e

    return result