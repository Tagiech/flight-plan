import threading

from handlers.actualize_calendar_handler import ActualizeCalendarHandler
from services.telegram_logger import TelegramLogger


def periodic_update():
    logger = TelegramLogger()
    try:
        ActualizeCalendarHandler().handle()
        threading.Timer(3600.0, periodic_update).start()
    except BaseException as exc:
        logger.log_exception(exc)
        threading.Timer(3600.0, periodic_update).start()


if __name__ == '__main__':
    thread = threading.Thread(target=periodic_update)
    thread.start()
    thread.join()
