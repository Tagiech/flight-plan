import traceback
from datetime import datetime

import telebot
from configs.config import API_TOKEN, CHAT_ID


class TelegramLogger:

    def __init__(self):
        self.__bot = telebot.TeleBot(API_TOKEN)

    def log_information(self, message: str):
        str_now = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.__bot.send_message(CHAT_ID, "Level: Information \n"
                                         f"Timestamp: {str_now}\n" + message)

    def log_changes_in_calendar(self, new_events_qty: int, removed_events_qty: int, details_message: str = ""):
        str_now = datetime.now().strftime("%d.%m.%Y %H:%M")
        message = (f"Created {new_events_qty} new events\n"
                   f"Deleted {removed_events_qty} events")
        self.__bot.send_message(CHAT_ID, "Level: Information \n"
                                         f"Timestamp: {str_now}\n" + message + '\n' + details_message)

    def log_error(self, message: str):
        str_now = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.__bot.send_message(CHAT_ID, "Level: Error \n"
                                         f"Timestamp: {str_now}\n" + message)

    def log_exception(self, exception: BaseException):
        str_now = datetime.now().strftime("%d.%m.%Y %H:%M")
        traceback_strs = traceback.format_exception(type(exception), exception, exception.__traceback__)
        message = traceback_strs[0]
        for i in range(1, len(traceback_strs)):
            message += '\n\n' + traceback_strs[i]

        self.__bot.send_message(CHAT_ID, "Level: Error \n"
                                         f"Timestamp: {str_now}\n"
                                         f"Caught unhandled exception: \n\n" + message)

    def log_exception_with_image(self, exception: BaseException, image_name: str):
        str_now = datetime.now().strftime("%d.%m.%Y %H:%M")
        traceback_strs = traceback.format_exception(type(exception), exception, exception.__traceback__)
        message = traceback_strs[0]
        for i in range(1, len(traceback_strs)):
            message += '\n\n' + traceback_strs[i]

        self.__bot.send_photo(CHAT_ID, open(image_name, 'rb'), "Level: Error \n"
                                                               f"Timestamp: {str_now}\n"
                                                               f"Caught unhandled exception: \n\n" + message)
