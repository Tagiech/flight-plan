from datetime import datetime, timedelta

from domain.flight import Flight
from domain.reserve import Reserve
from domain.work_event import WorkEvent


class CalendarEvent:
    summary: str
    description: str
    start: datetime
    end: datetime
    color: int

    def __init__(self, flight: Flight):
        if len(flight.airports) > 2:
            self.summary = f"Командировка в {flight.airports[0]}"
        else:
            self.summary = f"Полёт в {flight.airports[0]}"

        time_in_flight = str(flight.arrival_date_time - flight.departure_date_time)[:-3]

        self.description = f"Аэропорты: {flight.airports} \n" + \
                           f"Номера полетов: {flight.flight_number} \n" + \
                           f"Самолёт: {flight.plane_model} \n" + \
                           f"Вылет: {flight.departure_date_time.strftime('%Y-%m-%d %H:%M')} \n" + \
                           f"Прилёт: {flight.arrival_date_time.strftime('%Y-%m-%d %H:%M')} \n" + \
                           f"Время в рейсе: {time_in_flight}"

        self.start = flight.departure_date_time - datetime.timedelta(hours=2)
        self.end = flight.arrival_date_time

        start_distance_from_day_begin = self.start - datetime(self.start.year, self.start.month, self.start.day)
        begin_gap = timedelta(seconds=0 * 60 * 60 + 30 * 60)
        end_gap = timedelta(seconds=5 * 60 * 60 + 30 * 60)
        if begin_gap < start_distance_from_day_begin < end_gap:
            self.color = 10
        else:
            self.color = 7

    def __init__(self, reserve: Reserve):
        self.summary = "Резерв"
        self.description = reserve.info
        self.start = reserve.begin_date_time
        self.end = reserve.end_date_time
        self.color = 5

    def __init__(self, event: WorkEvent):
        self.summary = event.info
        self.description = ""
        self.start = event.begin_date_time
        self.end = event.end_date_time
        self.color = 3

    def toJson(self):
        return {
            'summary': self.summary,
            'description': self.description,
            'colorId': str(self.color),
            'start': {
                'dateTime': self.start.astimezone().isoformat(),
            },
            'end': {
                'dateTime': self.end.astimezone().isoformat(),
            }
        }
