from flask import request, jsonify
import asyncio
from configuration.config import server_port, local_host, super_admin_token
from db_sqlalchemy.db_functions import *


from exception_types import DBException
from db_sqlalchemy.manytomany.db_server import myApp

from aiogram import Bot, Dispatcher
from flask_cors import cross_origin

import base64


# init DB from scratch
def init_DB_from_scratch():
    drop_cascade_all()
    print('Init DB from scratch with super admin')
    insert_admin_and_token(super_admin_name, super_admin_password, super_admin_token)

def run_app():
    app_obj = myApp()
    app = app_obj.app
    connDBParams_obj = app_obj.connDBParams_obj
    bot = Bot(token=app_obj.MY_TOKEN)
    dp = Dispatcher(bot)
    DBErrorReply = "DB_error_reply"
    GeneralErrorReplay = "general_error_reply"

    init_DB_from_scratch()
    def decode_base64(message_bytes):
        message_bytes = base64.b64decode(message_bytes)
        translated_message = message_bytes.decode('utf-8')
        return translated_message
    def encode_base64(message):
        message_bytes = message.encode('utf-8')
        message_bytes = base64.b64encode(message_bytes)
        message_encrypt = message_bytes.decode('utf-8')
        return message_encrypt

    @app.route("/")
    async def index():
        return "PollsBot Server :)" \
               "\nSearch PollsBot channel on telegram"

    ## ***********************************************users post ***********************************************
    @app.route('/register_user', methods=['POST'])
    def register_user():
        print('in register user post 1')
        try:
            data = request.get_json(force=True)
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
            data = request.get_json(force=True)
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
            data = request.get_json(force=True)
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
            data = request.get_json(force=True)
            poll_id_telegram = data['poll_id_telegram']
            chat_id = data['chat_id']
            answer_number = data['answer_number']
            print('poll_id_telegram : ', poll_id_telegram)
            print('chat_id : ', chat_id)
            print('answer_number : ', str(answer_number))
            try:
                id_poll_exists, id_poll = getIdPollByPollIdTelegram(poll_id_telegram)
                print(id_poll_exists, id_poll)
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

    ## ***********************************************admin - super admin - post ***********************************************
    # not an UI request
    @app.route('/remove_admin', methods=['POST'])
    def remove_admin():
        try:
            data = request.get_json(force=True)
            admin_name = data['admin_name']
            password = decode_base64(data['password'])
            try:
                if admin_name == super_admin_name and password == super_admin_password:
                    removed = delete_admin(admin_name, password)
                    if removed == 0:
                        send_back = 'There isn\'t a valid admin with this name on this device to remove'
                        return jsonify(message_back=send_back)

                    send_back = 'Admin have been removed '
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'You are not the super admin'
                    return jsonify(error=send_back)

            except DBException as e:
                print(e)
                send_back = DBErrorReply
                return jsonify(error=send_back), 400

        except Exception as e:
            send_back = GeneralErrorReplay
            return jsonify(error=send_back), 500
    ## ***********************************************admin post ***********************************************
    @app.route('/login_admin', methods=['POST'])
    @cross_origin()
    def login_admin():
        try:
            data = request.get_json(force=True)
            admin_name = data['admin_name']
            password = decode_base64(data['password'])
            try:
                token_exists, token_name = getTokenAndNameByAdminNamePasswordAndUpdate(admin_name, password)
                if token_exists:
                    token = token_name[0]
                    token = encode_base64(token)
                    admin_name = encode_base64(token_name[1])
                    response = jsonify(token=token, admin_name=admin_name)
                    print('user logged in')
                    return response
                else:
                    send_back = "admin not exists"
                    response = jsonify(error=send_back)
                    return response
            except DBException as e:
                print(e)
                send_back = GeneralErrorReplay
                response = jsonify(error=send_back)
                return response
        except Exception as e:
            print(e)
            send_back = GeneralErrorReplay
            response = jsonify(error=send_back)
            # response.headers.add("Access-Control-Allow-Origin", "*")
            return response

    @app.route('/logout_admin', methods=['POST'])
    @cross_origin()
    def logout_admin():
        try:
            data = request.get_json(force=True)
            token = decode_base64(data['token'])
            try:
                loged_out = logOutAndUpdateToken(token)
                if loged_out:
                    response = jsonify(message_back="logged out")
                    print('user logged out')
                    return response
                else:
                    send_back = "admin not exists"
                    response = jsonify(error=send_back)
                    return response
            except DBException as e:
                print(e)
                send_back = GeneralErrorReplay
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
        try:
            data = request.get_json(force=True)
            new_admin_name = data['admin_name']
            password = decode_base64(data['password'])
            token = decode_base64(data['token'])
            try:
                if is_a_admin_token(token):
                    is_admin = is_a_admin(new_admin_name)
                    if is_admin:
                        send_back = "Sorry, admin name already taken, try a different one"
                        response = jsonify(error=send_back)
                        return response
                    new_token = insert_admin(new_admin_name, password)
                    if new_token is not None:
                        send_back = new_token
                        response = jsonify(token=send_back)
                        return response
                else:
                    send_back = "You must be an admin to add admins"
                    response = jsonify(error=send_back)
                    return response
            except DBException as e:
                print(e)
                send_back = "Sorry, admin name already taken, try a different one"
                response = jsonify(error=send_back)
                return response
        except Exception as e:
            print(e)
            send_back = GeneralErrorReplay
            response = jsonify(error=send_back)
            #response.headers.add("Access-Control-Allow-Origin", "*")
            return response

    @app.route('/my_name_admin', methods=['POST'])
    def my_name_admin():
        try:
            data = request.get_json(force=True)
            token = decode_base64(data['token'])
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

    @app.route('/admins_name_list', methods=['POST'])
    @cross_origin()
    def admins_name_list():
        try:
            data = request.get_json(force=True)
            token = decode_base64(data['token'])
            try:
                if is_a_admin_token(token):
                    admins_list_exists, admins_list = getAdminsList()
                    if admins_list_exists:
                        send_back = admins_list
                        return jsonify(result_lst=send_back)
                    else:
                        send_back = 'This admin isn\'t registered!'
                        return jsonify(error=send_back)
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

    ## ***********************************************poll - super admin - post ***********************************************
    @app.route('/remove_poll', methods=['POST'])
    def remove_poll():
        try:
            data = request.get_json(force=True)
            admin_name = data['admin_name']
            password = decode_base64(data['password'])
            id_poll = data['id_poll']
            try:
                if admin_name == super_admin_name and password == super_admin_password:
                    removed = delete_poll(id_poll)
                    if removed == 0:
                        send_back = 'There isn\'t a valid admin_poll to remove'
                        return jsonify(message_back=send_back)

                    send_back = 'poll have been removed '
                    return jsonify(message_back=send_back)
                else:
                    send_back = 'You are not the super admin'
                    return jsonify(error=send_back)

            except DBException as e:
                print(e)
                send_back = DBErrorReply
                return jsonify(error=send_back), 400

        except Exception as e:
            send_back = GeneralErrorReplay
            return jsonify(error=send_back), 500

    ## ***********************************************poll post ***********************************************
    async def send_a_poll(users_chat_id_lst, poll_content, numbers_choices_dict):

        answers_lst = list(numbers_choices_dict.values())
        poll_id_telegram_lst = []
        # await dp.bot.send_message(1332261387, 'gfgfdgdf')
        for chat_id in users_chat_id_lst:  # send poll to all requested users
            try:
                poll_sent = await dp.bot.send_poll(
                    chat_id,
                    poll_content,
                    answers_lst,
                    is_anonymous=False,
                    allows_multiple_answers=False
                )
                poll_id_telegram = poll_sent["poll"]["id"]
                poll_id_telegram_lst.append(poll_id_telegram)
            except Exception as e:
                print(f'user {chat_id} error:')
                print(e)
        return poll_id_telegram_lst

    async def send_a_poll_and_register_to_poll_telegram(id_poll, users_chat_id_lst, poll_content, numbers_choices_dict):
        poll_id_telegram_lst = await send_a_poll(users_chat_id_lst, poll_content, numbers_choices_dict)
        for poll_id_telegram in poll_id_telegram_lst:
            insert_poll_telegram(id_poll,
                                 poll_id_telegram)  # token admin exists because registration poll is from the UI
        return True

    @app.route('/register_and_send_poll', methods=['POST'])
    @cross_origin()
    def register_and_send_poll():
        try:
            data = request.get_json(force=True)
            token = decode_base64(data['token'])
            poll_content = data['poll_content']
            numbers_choices_dict = transformNumberAnswerListToDict(data['numbers_choices_lst'])
            idPoll_answer_lst = data['idPoll_answer_lst']
            should_union = data['should_union']
            users_chat_id_lst= []

            try:
                if is_a_admin_token(token):
                    is_idPoll_answer_lst_empty = len(idPoll_answer_lst) == 0 # or 'data' not in idPoll_answer_lst[0]
                    if is_idPoll_answer_lst_empty or ('data' in idPoll_answer_lst[0] and idPoll_answer_lst[0]['data'] == ""):
                        # no filtering
                        users_chat_id_lst = getAllUsersChatIdsLst()
                        print('This is full list ', users_chat_id_lst)
                    else:
                        # filter
                        users_chat_id_lst = getChatIdLstToSend(idPoll_answer_lst, union=should_union)
                        print('This is filter list ', users_chat_id_lst)
                    if len(users_chat_id_lst) == 0:
                        send_back = 'No users at the mailing list for the poll.\n' \
                                    'Try other filtering or no filter at all'
                        return jsonify(error=send_back)
                    # register poll
                    id_poll, poll_content = insert_poll(poll_content, numbers_choices_dict)
                    insert_admin_poll(token, id_poll)  # token admin exists because registration poll is from the UI
                    send_back = 'poll have been registered'
                    # send a poll
                    asyncio.set_event_loop(asyncio.new_event_loop())
                    loop = asyncio.get_event_loop()
                    res_sending = loop.run_until_complete(send_a_poll_and_register_to_poll_telegram(id_poll, users_chat_id_lst,poll_content, numbers_choices_dict))
                    if res_sending:
                        send_back = 'Poll has been sent'
                        return jsonify(message_back=send_back)
                    else:
                        send_back = "Sorry, an error occurred, poll has\'nt been sent to all users"
                        return jsonify(error=send_back)
                else:
                    send_back = "Sorry, an error occurred, poll has\'nt been registered"
                    return jsonify(error=send_back)
            except ParsingException as e:
                print(e)
                send_back = "Error while parsing your input at the server"
                return jsonify(error=send_back), 400
            except UseException as e:
                print(e)
                send_back = "Each answer of the poll must be unique!"
                return jsonify(error=send_back)
            except DBException as e:
                print(e)
                send_back = DBErrorReply
                return jsonify(error=send_back), 400

        except Exception as e:
            print(e)
            send_back = GeneralErrorReplay
            return jsonify(error=send_back), 500


    @app.route('/get_poll_details', methods=['POST'])
    @cross_origin()
    def get_poll_details():
        try:
            data = request.get_json(force=True)
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
    ## ***********************************************data polls and answers post ***********************************************
    @app.route('/get_poll_answers', methods=['POST'])
    @cross_origin()
    def get_poll_answers():
        try:
            data = request.get_json(force=True)
            token = decode_base64(data['token'])
            id_poll = data['id_poll']
            try:
                print(id_poll)
                answers_hist_exists, answers_hist_dict = creatHistogramForSpecificPoll(token, id_poll)
                print(answers_hist_exists, answers_hist_dict)

                if answers_hist_exists:

                    send_back = answers_hist_dict
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

    @app.route('/get_associated_polls', methods=['POST'])
    @cross_origin()
    def get_associated_polls():
        try:
            data = request.get_json(force=True)
            token = decode_base64(data['token'])
            try:
                if is_a_admin_token(token):
                    associated_polls_exist, associated_polls = getAssociatesPollsToAdmin(token)
                    print(associated_polls_exist, associated_polls)
                    if associated_polls_exist:
                        if len(associated_polls) == 0:
                            send_back = "You don't have polls yet"
                            return jsonify(error=send_back)
                        else:
                            send_back = associated_polls
                            return jsonify(result_lst=send_back)

                    else:
                        # send_back =  "No polls to filter from"
                        # return jsonify(result_lst=send_back)
                        #send_back = [{'poll_content': 'poll1?', 'date': '2022-01-13', 'numbers_answers_lst': ['choice0', 'choice1', 'choice2'], 'id_poll': 1}, {'poll_content': 'poll3?', 'date': '2022-01-13', 'numbers_answers_lst': ['choice0', 'choice1', 'choice2'], 'id_poll': 3}]
                        send_back = []
                        return jsonify(result_lst=send_back)
                else:
                    send_back = "You Are not An Admin"
                    return jsonify(error=send_back), 404

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
