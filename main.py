# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import logging
from multiprocessing import Process

from db_utils.db_conn import UserDB
from exception_types import DBException
from telegram_handle.async_bot import startBot
from server.main_server import main_server

#import threading

# flask server = main server
def procss_main_server(name):
    logging.info("Process server %s: starting", name)
    main_server()
    logging.info("Process server %s: finishing", name)

#telegram bot server
def procss_telegram_bot(name):
    logging.info("Process telegram bot %s: starting", name)
    startBot()()
    logging.info("Process telegram bot %s: finishing", name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        # initial DB bt sql script
        UserDB().init_DB()
    except DBException as e:
        print("DB initial error")

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # main server
    main_server_process = Process(target=procss_main_server, args=(1,))
    #main_server_process = threading.Thread(target=procss_main_server, args=(1,))
    main_server_process.start()
    # main_server.join()


    # telegram bot
    telegram_bot_process = Process(target=procss_telegram_bot, args=(2,))
    #telegram_bot_process = threading.Thread(target=procss_telegram_bot, args=(2,))
    telegram_bot_process.start()
    # telegram_bot.join()








