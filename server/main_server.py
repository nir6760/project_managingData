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

        # connDBParams_obj.session_destroy()
        # return "<p>all dropped</p>"
        return response


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

    app.run(threaded=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_app()
