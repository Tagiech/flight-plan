import threading

from handlers.actualize_calendar_handler import ActualizeCalendarHandler


def periodic_update():
    ActualizeCalendarHandler().handle()
    threading.Timer(3600.0, periodic_update).start()


if __name__ == '__main__':
    thread = threading.Thread(target=periodic_update)
    thread.start()
    thread.join()
