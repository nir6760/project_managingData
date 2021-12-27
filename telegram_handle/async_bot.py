"""
This is a echo bot.
It echoes any incoming text messages.
"""
import json
import logging

from aiogram import Bot, Dispatcher, executor, types

from db_utils.db_conn import UserDB
from exception_types import InvalidUserNameException, DBException

#request python
import requests


class MyBot:
    def __init__(self):
        self.API_TOKEN = "5062861976:AAFl2UAliIU4I5a4JS16SU6X82dOdHcD7cU"
        self.MY_SERVER_PATH = "http://127.0.0.1:5000"
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        # Initialize bot and dispatcher
        self.bot = Bot(token=self.API_TOKEN)
        self.dp = Dispatcher(self.bot)
        self.help_reply = \
            '''/register <user-name> -Register to start
answering polls via telegram
<user-name> in smart polling system

/remove <user-name> -To stop getting polls
queries
<user-name> in smart polling system

/MyName -To get the user name for this device
if the device is registered to service

/start or /help -Use start or help anytime to see this menu again
                '''
        self.error_reply = 'An Error occurred, please try again later'


# main function to start bot
def startBot():
    my_bot = MyBot()
    dp = my_bot.dp

    @dp.callback_query_handler()
    async def callback_query_handler(call_back):
        cqd = call_back.data
        print(cqd)
        # message_id = update.callback_query.message.message_id
        # update_id = update.update_id
        if cqd['callback'] == "/register":
            await register(cqd['input_message'])
        # elif cqd == ... ### for other buttons

    # bot sends welcome for start
    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        """
        This handler will be called when user sends `/start` command
        """
        name = ""
        if (message.from_user.first_name is not None):
            name = message.from_user.first_name
            if (message.from_user.last_name is not None):
                name += message.from_user.last_name
        hello_str = f'''Hello, {name}.
'''
        welcome_str = \
            '''Welcome to smart Polling.
Please choose one of the options:
'''
        await message.reply(hello_str)
        await message.reply(welcome_str)
        await message.reply(my_bot.help_reply)

    # bor sends help
    @dp.message_handler(commands=['help'])
    async def send_help(message: types.Message):
        """
        This handler will be called when user sends `/help` command
        """
        # keyboard = types.InlineKeyboardMarkup()
        # keyboard.add(types.InlineKeyboardButton('Register',callback_data = call_data))
        # # keyboard.add(types.InlineKeyboardButton('Remove', url='/remove'))
        # await message.reply(
        #                     '1) To register Polls service press /register.\n' +
        #                     '2) To remove from Polls service press /remove'
        #                     ,
        #                     reply_markup=keyboard
        #                     )

        await message.reply(my_bot.help_reply)

    # parse the user name from register or remove request
    def parse_user_name(str):
        str_lst = str.split(' ', 1)
        if len(str_lst) != 2:
            raise InvalidUserNameException
        return str_lst[1]

    async def sendFormatErrorToUser(message):
            await message.reply(
                '''Sorry, format is invalid,
You can always get help by /help'''
            )

    # function helper for printing
    def user_info(message):
        print(
            '******************************************my propertoes are:  ***********************************************')
        print(message.text)
        print(message.from_user.id)
        print(message.chat.id)
        print(message.from_user.first_name)
        print(message.from_user.last_name)
        print(message.from_user.username)

    @dp.message_handler(commands=['register'])
    async def register(message: types.Message):
        try:
            chat_id = str(message.chat.id)
            user_name = parse_user_name(message.text)

            request_res = requests.post(my_bot.MY_SERVER_PATH + '/register_user'
                              , json={'chat_id': chat_id, 'user_name': user_name})

            message_back = json.loads(request_res.content.decode('utf8'))
            if message_back['message_back'] == "general_error_reply":
                await message.reply(my_bot.error_reply)
            else:
                await message.reply(message_back['message_back'])

        except InvalidUserNameException as e:
            await sendFormatErrorToUser(message)
        except Exception as e:
            print(e)
            await message.reply(my_bot.error_reply)

    @dp.message_handler(commands=['remove'])
    async def remove(message: types.Message):
        try:
            chat_id = str(message.chat.id)
            user_name = parse_user_name(message.text)

            request_res = requests.post(my_bot.MY_SERVER_PATH + '/remove_user'
                                        , json={'chat_id': chat_id, 'user_name': user_name})

            message_back = json.loads(request_res.content.decode('utf8'))
            if message_back['message_back'] == "general_error_reply":
                await message.reply(my_bot.error_reply)
            else:
                await message.reply(message_back['message_back'])

        except InvalidUserNameException as e:
            await sendFormatErrorToUser(message)
        except Exception as e:
            print(e)
            await message.reply(my_bot.error_reply)

    @dp.message_handler(commands=['MyName'])
    async def remove(message: types.Message):
        try:
            chat_id = str(message.chat.id)
            #user_name = parse_user_name(message.text)
            request_res = requests.post(my_bot.MY_SERVER_PATH + '/my_name_user'
                                        , json={'chat_id': chat_id})

            message_back = json.loads(request_res.content.decode('utf8'))
            if message_back['message_back'] == "general_error_reply":
                await message.reply(my_bot.error_reply)
            else:
                await message.reply(message_back['message_back'])

        except InvalidUserNameException as e:
            await sendFormatErrorToUser(message)
        except Exception as e:
            print(e)
            await message.reply(my_bot.error_reply)

    # send error format for each non recognized request
    @dp.message_handler()
    async def echo(message: types.Message):
        # old style:
        # await bot.send_message(message.chat.id, message.text)

        await sendFormatErrorToUser(message)

    # run the bot async
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    startBot()
