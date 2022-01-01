"""
This is a echo bot.
It echoes any incoming text messages.
"""
import json
import logging

from aiogram import Bot, Dispatcher, executor, types

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
    async def my_name(message: types.Message):
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

    @dp.message_handler(commands=['poll'])
    async def poll(message_user: types.Message) -> None:
        """Sends a predefined poll"""
        answers = ["Good", "Really good", "Fantastic", "Great"]
        poll = await my_bot.bot.send_poll(
            message_user.chat.id,
            "How are you?",
            answers,
            is_anonymous=False,
            allows_multiple_answers=False,
        )
        # Save some info about the poll the bot_data for later use in receive_poll_answer
        payload = {
            poll.poll.id: {
                "questions": answers,
                "message_id": poll.message_id,
                "chat_id": message_user.chat.id,
                "answer": poll,
            }
        }
        my_bot.dp.data.update(payload)

    @dp.poll_answer_handler()
    async def receive_poll_answer(message_user: types.Message) -> None:
        """Summarize a users poll vote"""
        bot_data = my_bot.dp.data

        try:
            poll_id = message_user['poll_id']
            user_poll = message_user['user']
            ans_lst = bot_data[poll_id]['questions']
            answer = ans_lst[message_user['option_ids'][0]]
            print(user_poll, answer)
        # this means this poll answer update is from an old poll, we can't do our answering then
        except KeyError:
            return
        # selected_options = answer.option_ids
        # answer_string = ""
        # for question_id in selected_options:
        #     if question_id != selected_options[-1]:
        #         answer_string += questions[question_id] + " and "
        #     else:
        #         answer_string += questions[question_id]
        # context.bot.send_message(
        #     context.bot_data[poll_id]["chat_id"],
        #     f"{update.effective_user.mention_html()} feels {answer_string}!",
        #     parse_mode=ParseMode.HTML,
        # )
        # context.bot_data[poll_id]["answers"] += 1
        # # Close poll after three participants voted
        # if context.bot_data[poll_id]["answers"] == 3:
        #     context.bot.stop_poll(
        #         context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
        #     )

    # send error format for each non recognized request
    @dp.message_handler()
    async def echo(message: types.Message):
        # old style:
        # await bot.send_message(message.chat.id, message.text)

        await sendFormatErrorToUser(message)



    # run the bot async
    executor.start_polling(dp, skip_updates=False)


if __name__ == '__main__':
    startBot()
