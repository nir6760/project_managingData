import telegram
from flask import request, jsonify
from db_sqlalchemy.db_functions import *

from exception_types import DBException
from db_sqlalchemy.manytomany.db_server import myApp

from aiogram import Bot, Dispatcher, executor, types
from flask_cors import cross_origin


def run_app():
    app_obj = myApp()
    app = app_obj.app
    connDBParams_obj = app_obj.connDBParams_obj
    bot = Bot(token=app_obj.MY_TOKEN)
    dp = Dispatcher(bot)

    @app.route("/")
    async def index():
        response = jsonify(message="Simple server is running")
        # Enable Access-Control-Allow-Origin
        response.headers.add("Access-Control-Allow-Origin", "*")

        #
        answers = ["Good", "Really good", "Fantastic", "Great"]
        # await dp.bot.send_message(1332261387, 'gfgfdgdf')

        m = await dp.bot.send_poll(
            "1332261387",
            "How are you?",
            answers,
            is_anonymous=False,
            allows_multiple_answers=False
        )
        print(m.poll)
        # poll = {"id": "5969670530423324700", "question": "How are you?",
        #  "options": [{"text": "Good", "voter_count": 0}, {"text": "Really good", "voter_count": 0},
        #              {"text": "Fantastic", "voter_count": 0}, {"text": "Great", "voter_count": 0}],
        #  "total_voter_count": 0, "is_closed": false, "is_anonymous": false, "type": "regular",
        #  "allows_multiple_answers": false}

        # connDBParams_obj.session_destroy()
        # return "<p>all dropped</p>"
        return response

    ## ***********************************************users post ***********************************************
    @app.route('/register_user', methods=['POST'])
    @cross_origin()
    def register_user():
        print('in register user post 1')
        try:
            data = request.json
            print('in register user post 2')
            print(data)
            chat_id = data['chat_id']
            user_name = data['user_name']
            try:
                is_user = is_a_user(chat_id, user_name)
                if is_user:
                    send_back = 'This device is already registered!'
                    return jsonify(message_back=send_back)
                insert_user(chat_id, user_name)

                send_back = 'You have been registered'
                return jsonify(message_back=send_back)

            except DBException as e:
                print(e)
                send_back = "general_error_reply"
                return jsonify(message_back=send_back)

        except Exception as e:
            print(e)
            send_back = "general_error_reply"
            return jsonify(message_back=send_back)

    @app.route('/remove_user', methods=['POST'])
    def remove_user():
        try:
            data = request.json
            chat_id = data['chat_id']
            user_name = data['user_name']
            print('request is ' + str(data))
            try:

                removed = delete_user(chat_id, user_name)
                if removed == 0:
                    send_back = 'There isn\'t a valid user with this name on this device to remove'
                    return jsonify(message_back=send_back)

                send_back = 'You have been removed :('
                return jsonify(message_back=send_back)

            except DBException as e:
                print(e)
                send_back = "general_error_reply"
                return jsonify(message_back=send_back)

        except Exception as e:
            send_back = "general_error_reply"
            return jsonify(message_back=send_back)

    @app.route('/my_name_user', methods=['POST'])
    def my_name():
        try:
            data = request.json
            chat_id = data['chat_id']
            try:

                user_name_exists, user_name = getUserName(chat_id)

                if user_name_exists:
                    user_name_str = user_name
                    send_back = f'User Name is {user_name_str}'
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'This device isn\'t registered!'
                    return jsonify(message_back=send_back)

            except DBException as e:
                print(e)
                send_back = "general_error_reply"
                return jsonify(message_back=send_back)

        except Exception as e:
            send_back = "general_error_reply"
            return jsonify(message_back=send_back)

    ## ***********************************************admin post ***********************************************
    @app.route('/register_admin', methods=['POST'])
    @cross_origin()
    def register_admin():
        try:
            data = request.json
            email_admin = data['email_admin']
            password = data['password']
            admin_name = data['admin_name']
            try:
                is_admin = is_a_admin(email_admin)
                if is_admin:
                    send_back = 'This admin is already registered!'
                    return jsonify(message_back=send_back)
                insert_admin(email_admin, password, admin_name)

                send_back = 'You have been registered'
                return jsonify(message_back=send_back)

            except DBException as e:
                print(e)
                send_back = "general_error_reply"
                return jsonify(error=send_back)

        except Exception as e:
            print(e)
            send_back = "general_error_reply"
            return jsonify(error=send_back)

    @app.route('/remove_admin', methods=['POST'])
    def remove_admin():
        try:
            data = request.json
            email_admin = data['email_admin']
            password = data['password']
            try:

                removed = delete_admin(email_admin, password)
                if removed == 0:
                    send_back = 'There isn\'t a valid admin with this name on this device to remove'
                    return jsonify(message_back=send_back)

                send_back = 'Admin have been removed '
                return jsonify(message_back=send_back)

            except DBException as e:
                print(e)
                send_back = "general_error_reply"
                return jsonify(error=send_back)

        except Exception as e:
            send_back = "general_error_reply"
            return jsonify(error=send_back)

    @app.route('/my_name_admin', methods=['POST'])
    def my_name_admin():
        try:
            data = request.json
            email_admin = data['email_admin']
            try:

                admin_name_exists, admin_name = getAdminName(email_admin)

                if admin_name_exists:
                    admin_name_str = admin_name
                    send_back = admin_name_str
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'This admin isn\'t registered!'
                    return jsonify(error=send_back)

            except DBException as e:
                print(e)
                send_back = "general_error_reply"
                return jsonify(error=send_back)

        except Exception as e:
            send_back = "general_error_reply"
            return jsonify(error=send_back)

    @app.route('/get_associates_polls', methods=['POST'])
    def get_associates_polls():
        try:
            data = request.json
            email_admin = data['email_admin']
            password = data['password'] #no need email and password for details
            try:
                associates_polls_exists, associates_polls_lst = getAssociatesPollsToAdminPassword(email_admin, password)

                if associates_polls_exists:
                    send_back = associates_polls_lst
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'This admin has\'nt  any polls'
                    return jsonify(error=send_back)

            except DBException as e:
                print(e)
                send_back = "general_error_reply"
                return jsonify(error=send_back)

        except Exception as e:
            send_back = "general_error_reply"
            return jsonify(error=send_back)


    def send_a_poll(users_chat_id_lst, poll_content, numbers_choices_dict):
        answers_lst = list(numbers_choices_dict.values())
        id_poll = None
        # await dp.bot.send_message(1332261387, 'gfgfdgdf')
        for chat_id in users_chat_id_lst:
            poll_sent = await dp.bot.send_poll(
                "1332261387",
                poll_content,
                answers_lst,
                is_anonymous=False,
                allows_multiple_answers=False
            )
            id_poll = poll_sent


    ## ***********************************************poll post ***********************************************
    @app.route('/register_poll', methods=['POST'])
    @cross_origin()
    def register_and_send_poll():
        try:
            data = request.json
            email_admin = data['email_admin']
            id_poll = data['id_poll']
            poll_content = data['poll_content']
            numbers_choices_dict = data['numbers_choices_dict']

            users_chat_id_lst = data['users_chat_id_lst']

            try:
                is_poll = is_a_poll(id_poll)
                if is_poll:
                    send_back = 'This poll is already registered!'
                    return jsonify(error=send_back)
                insert_poll(poll_content, numbers_choices_dict)

                insert_admin_poll(email_admin, id_poll)  # email admin exists because registration poll is from the UI

                send_back = 'poll have been registered'
                return jsonify(message_back=send_back)
            except UseException as e:
                print(e)
                send_back = "use exception, answers must be unique"
                return jsonify(error=send_back)
            except DBException as e:
                print(e)
                send_back = "general_error_reply"
                return jsonify(error=send_back)

        except Exception as e:
            print(e)
            send_back = "general_error_reply"
            return jsonify(error=send_back)

    @app.route('/remove_poll', methods=['POST'])
    def remove_poll():
        try:
            data = request.json
            email_admin = data['email_admin']
            password = data['password']
            id_poll = data['id_poll']
            try:

                removed = delete_poll_from_admin(email_admin, password, id_poll)
                if removed == 0:
                    send_back = 'There isn\'t a valid admin_poll to remove'
                    return jsonify(message_back=send_back)

                send_back = 'poll have been removed '
                return jsonify(message_back=send_back)

            except DBException as e:
                print(e)
                send_back = "general_error_reply"
                return jsonify(error=send_back)

        except Exception as e:
            send_back = "general_error_reply"
            return jsonify(error=send_back)

    @app.route('/get_poll_details', methods=['POST'])
    def get_poll_details():
        try:
            data = request.json
            # email_admin = data['email_admin']
            # password = data['password'] #no need email and password for details
            id_poll = data['id_poll']
            try:
                poll_data_exists, poll_data_dict = getFullPollData(id_poll)

                if poll_data_exists:
                    send_back = poll_data_dict
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'This poll isn\'t registered!'
                    return jsonify(error=send_back)

            except DBException as e:
                print(e)
                send_back = "general_error_reply"
                return jsonify(error=send_back)

        except Exception as e:
            send_back = "general_error_reply"
            return jsonify(error=send_back)

    @app.route('/get_poll_answers', methods=['POST'])
    def get_poll_answers():
        try:
            data = request.json
            email_admin = data['email_admin']
            password = data['password'] # need email and password for answers
            id_poll = data['id_poll']
            try:
                answers_data_exists, answers_data_dict = getAnswersForPollByAdmin(email_admin, password, id_poll)

                if answers_data_exists:
                    send_back = answers_data_dict
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'This poll isn\'t registered!'
                    return jsonify(error=send_back)

            except DBException as e:
                print(e)
                send_back = "general_error_reply"
                return jsonify(error=send_back)

        except Exception as e:
            send_back = "general_error_reply"
            return jsonify(error=send_back)



    app.run(threaded=True)

telegram.poll.Poll()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_app()
