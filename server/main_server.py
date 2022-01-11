import json

import telegram
from flask import request, jsonify

from configuration.config import server_port, local_host
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

    DBErrorReply = "DB_error_reply"
    GeneralErrorReplay = "general_error_reply"

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
                send_back = DBErrorReply
                return jsonify(message_back=send_back), 400

        except Exception as e:
            print(e)
            send_back = GeneralErrorReplay
            return jsonify(message_back=send_back), 500

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
                send_back = DBErrorReply
                return jsonify(message_back=send_back), 400

        except Exception as e:
            send_back = GeneralErrorReplay
            return jsonify(message_back=send_back), 500

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
                send_back = DBErrorReply
                return jsonify(message_back=send_back), 400

        except Exception as e:
            send_back = GeneralErrorReplay
            return jsonify(message_back=send_back), 500

    @app.route('/user_answer', methods=['POST'])
    def user_answer():
        try:
            data = request.json
            poll_id_telegram = data['poll_id_telegram']
            chat_id = data['chat_id']
            answer_number = data['answer_number']
            try:
                id_poll_exists, id_poll = getIdPollByPollIdTelegram(poll_id_telegram)
                if id_poll_exists:
                    insert_user_answer(chat_id, id_poll, answer_number)
                    send_back = 'Answer has been received'
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'something went wrong :('
                    return jsonify(message_back=send_back), 401

            except DBException as e:
                print(e)
                send_back = DBErrorReply
                return jsonify(message_back=send_back), 400

        except Exception as e:
            send_back = GeneralErrorReplay
            return jsonify(message_back=send_back), 500
    ## ***********************************************admin post ***********************************************
    @app.route('/login_admin', methods=['POST'])
    @cross_origin()
    def login_admin():
        try:
            data = request.get_json(force=True)
            admin_name = data['admin_name']
            password = data['password']
            try:
                token_exists, token_name = getTokenAndNameByAdminNamePassword(admin_name, password)
                if token_exists:
                    token = token_name[0]
                    admin_name = token_name[1]
                    response = jsonify(token=token, admin_name=admin_name)
                    return response
                else:
                    send_back = "admin name registered"
                    response = jsonify(error=send_back)
                    return response
            except DBException as e:
                print(e)
                send_back = "admin name must be unique"
                response = jsonify(error=send_back)
                return response
        except Exception as e:
            print(e)
            send_back = GeneralErrorReplay
            response = jsonify(error=send_back)
            # response.headers.add("Access-Control-Allow-Origin", "*")
            return response
    @app.route('/register_admin', methods=['POST'])
    @cross_origin()
    def register_admin():
        # send_back = 'worrkkkk!!!!!!'
        # response = app.response_class(
        #     response=json.dumps({"hey":"hey1"}),
        #     mimetype='application/json'
        # )
        # # response = jsonify(message_back=send_back)
        # # response.headers.add('Access-Control-Allow-Origin', '*')
        # # response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        # # response.headers.add('Access-Control-Allow-Methods', 'POST')
        # return response
        try:
            data = request.get_json(force=True)
            admin_name = data['admin_name']
            password = data['password']
            try:
                is_admin = is_a_admin(admin_name)
                if is_admin:
                    send_back = "sorry, user name already taken"
                    response = jsonify(error=send_back)
                    return response
                token = insert_admin(admin_name, password)
                if token is not None:
                    send_back = token
                    response = jsonify(token=send_back, admin_name=admin_name)
                    return response
                else:
                    send_back = "sorry, user name already taken"
                    response = jsonify(error=send_back)
                    return response
            except DBException as e:
                print(e)
                send_back = "sorry, user name already taken"
                response = jsonify(error=send_back)
                return response
        except Exception as e:
            print(e)
            send_back = GeneralErrorReplay
            response = jsonify(error=send_back)
            #response.headers.add("Access-Control-Allow-Origin", "*")
            return response

    @app.route('/remove_admin', methods=['POST'])
    def remove_admin():
        try:
            data = request.json
            admin_name = data['admin_name']
            password = data['password']
            try:

                removed = delete_admin(admin_name, password)
                if removed == 0:
                    send_back = 'There isn\'t a valid admin with this name on this device to remove'
                    return jsonify(message_back=send_back)

                send_back = 'Admin have been removed '
                return jsonify(message_back=send_back)

            except DBException as e:
                print(e)
                send_back = DBErrorReply
                return jsonify(error=send_back), 400

        except Exception as e:
            send_back = GeneralErrorReplay
            return jsonify(error=send_back), 500

    @app.route('/my_name_admin', methods=['POST'])
    def my_name_admin():
        try:
            data = request.json
            token = data['token']
            try:

                admin_name_exists, admin_name = getAdminNameByToken(token)

                if admin_name_exists:
                    admin_name_str = admin_name
                    send_back = admin_name_str
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'This admin isn\'t registered!'
                    return jsonify(error=send_back)

            except DBException as e:
                print(e)
                send_back = DBErrorReply
                return jsonify(error=send_back), 400

        except Exception as e:
            send_back = GeneralErrorReplay
            return jsonify(error=send_back), 500

    @app.route('/get_associates_polls', methods=['POST'])
    def get_associates_polls():
        try:
            data = request.json
            token = data['token']
            try:
                associates_polls_exists, associates_polls_lst = getAssociatesPollsToAdmin(token)

                if associates_polls_exists:
                    send_back = associates_polls_lst
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'This admin has\'nt  any polls'
                    return jsonify(error=send_back)

            except DBException as e:
                print(e)
                send_back = DBErrorReply
                return jsonify(error=send_back), 400

        except Exception as e:
            send_back = GeneralErrorReplay
            return jsonify(error=send_back), 500

    ## ***********************************************poll post ***********************************************

    @app.route('/register_poll', methods=['POST'])
    @cross_origin()
    def register_poll():
        try:
            data = request.json
            token = data['token']
            poll_content = data['poll_content']
            numbers_choices_dict = data['numbers_choices_dict']
            # poll_id_telegram = data['poll_id_telegram'] #for
            # users_chat_id_lst = data['users_chat_id_lst']

            try:
                id_poll = insert_poll(poll_content, numbers_choices_dict)
                insert_admin_poll(token, id_poll)  # token admin exists because registration poll is from the UI
                send_back = 'poll have been registered'
                return jsonify(message_back=send_back)
            except UseException as e:
                print(e)
                send_back = "use exception, answers must be unique"
                return jsonify(error=send_back)
            except DBException as e:
                print(e)
                send_back = DBErrorReply
                return jsonify(error=send_back), 400

        except Exception as e:
            print(e)
            send_back = GeneralErrorReplay
            return jsonify(error=send_back), 500

    async def send_a_poll(users_chat_id_lst, poll_content, numbers_choices_dict):
        answers_lst = list(numbers_choices_dict.values())
        poll_id_telegram_lst = []
        # await dp.bot.send_message(1332261387, 'gfgfdgdf')
        for chat_id in users_chat_id_lst:  # send poll to all requested users
            poll_sent = await dp.bot.send_poll(
                chat_id,
                poll_content,
                answers_lst,
                is_anonymous=False,
                allows_multiple_answers=False
            )
            poll_id_telegram = poll_sent["id"]
            poll_id_telegram_lst.append(poll_id_telegram)
        return poll_id_telegram_lst

    @app.route('/send_poll', methods=['POST'])
    @cross_origin()
    async def send_poll_and_register_poll_telegram():
        try:
            data = request.json
            token = data['token']
            id_poll = data['id_poll']
            poll_content = data['poll_content']
            numbers_choices_dict = data['numbers_choices_dict']
            users_chat_id_lst = data['users_chat_id_lst']
            try:
                if is_a_admin_token(token):
                    poll_id_telegram_lst = await send_a_poll(users_chat_id_lst, poll_content, numbers_choices_dict)
                    for poll_id_telegram in poll_id_telegram_lst:
                        insert_poll_telegram(id_poll, poll_id_telegram)  # email admin exists because registration poll is from the UI
                    send_back = 'poll have been sent'
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'this is not an admin request'
                    return jsonify(error=send_back), 401
            except UseException as e:
                print(e)
                send_back = "use exception, answers must be unique"
                return jsonify(error=send_back), 400
            except DBException as e:
                print(e)
                send_back = DBErrorReply
                return jsonify(error=send_back), 400

        except Exception as e:
            print(e)
            send_back = GeneralErrorReplay
            return jsonify(error=send_back), 500

    @app.route('/remove_poll', methods=['POST'])
    def remove_poll():
        try:
            data = request.json
            token = data['token']
            id_poll = data['id_poll']
            try:

                removed = delete_poll_by_admin(token, id_poll)
                if removed == 0:
                    send_back = 'There isn\'t a valid admin_poll to remove'
                    return jsonify(message_back=send_back)

                send_back = 'poll have been removed '
                return jsonify(message_back=send_back)

            except DBException as e:
                print(e)
                send_back = DBErrorReply
                return jsonify(error=send_back), 400

        except Exception as e:
            send_back = GeneralErrorReplay
            return jsonify(error=send_back), 500

    @app.route('/get_poll_details', methods=['POST'])
    def get_poll_details():
        try:
            data = request.json
            # token = data['token'] # no need to be admin  for poll details
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
                send_back = DBErrorReply
                return jsonify(error=send_back), 400

        except Exception as e:
            send_back = GeneralErrorReplay
            return jsonify(error=send_back), 500

    @app.route('/get_poll_answers', methods=['POST'])
    def get_poll_answers():
        try:
            data = request.json
            token = data['token']
            id_poll = data['id_poll']
            try:
                answers_data_exists, answers_data_dict = getAnswersForPollByAdmin(token, id_poll)

                if answers_data_exists:
                    send_back = answers_data_dict
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'This poll isn\'t registered!'
                    return jsonify(error=send_back)

            except DBException as e:
                print(e)
                send_back = DBErrorReply
                return jsonify(error=send_back), 400

        except Exception as e:
            send_back = GeneralErrorReplay
            return jsonify(error=send_back), 500

    app.run(host=local_host, port=server_port, threaded=True)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_app()
