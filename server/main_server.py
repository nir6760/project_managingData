from flask import Flask
from flask import Flask, request, jsonify
import telegram

from db_utils.db_conn import UserDB
from exception_types import DBException, InvalidUserNameException

MY_TOKEN = "5062861976:AAFl2UAliIU4I5a4JS16SU6X82dOdHcD7cU"
app = Flask(__name__)



@app.route("/")
def index():
    #bot = telegram.Bot(token=MY_TOKEN)
    #bot.send_message(chat_id="1332261387", text='USP-Python has started up!')
    return "<p>Admin UI! - Coming Soon</p>"

@app.route('/register_user', methods=['POST'])
def register_user():
    try:
        data = request.json
        chat_id = data['chat_id']
        user_name = data['user_name']
        try:
            with UserDB() as u:
                is_user = u.is_a_user(chat_id, user_name)
                if is_user:
                    send_back = 'This device is already registered!'
                    return jsonify(message_back=send_back)
                u.insert_user(chat_id, user_name)

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
            with UserDB() as u:
                removed = u.delete_user(chat_id, user_name)
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

            with UserDB() as u:
                user_name_exists, user_name = u.getUserName(chat_id)

                if user_name_exists:
                    user_name_str = user_name[0]
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


# main function to run server from process
def main_server():

    app.run(threaded=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_server()

