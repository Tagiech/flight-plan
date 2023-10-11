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

    def __init__(self, event: Flight | Reserve | WorkEvent):

        if type(event) == Flight:
            self.__create_flight(event)
        elif type(event) == Reserve:
            self.__create_reserve(event)
        elif type(event) == WorkEvent:
            self.__create_work_event(event)

    def __create_flight(self, flight: Flight):
        if len(flight.airports) > 2:
            self.summary = f"Командировка в {flight.airports[0]}"
        else:
            self.summary = f"Полёт в {flight.airports[0]}"
        airports = flight.airports[0][:1] + flight.airports[0][1:].lower()
        flight_numbers = flight.flight_number.replace('п', '').replace('FV', 'SU').split("/")
        links = "Пулково -> " + airports + ": https://flightradar24.com/" + flight_numbers[0] + "\n"
        for i in range(1, len(flight.airports)):
            previous_airport = (flight.airports[i - 1][:1] + flight.airports[i - 1][1:].lower()).replace(' [пас]', '')
            next_airport = flight.airports[i][:1] + flight.airports[i][1:].lower()
            airports += ', ' + next_airport
            links += previous_airport + " -> " + next_airport + ": https://flightradar24.com/" + flight_numbers[
                i] + "\n"

        time_in_flight = str(flight.arrival_date_time - flight.departure_date_time)[:-3]

        self.description = f"Аэропорты: {airports} \n" + \
                           f"Номера полетов: {flight.flight_number} \n" + \
                           f"Самолёт: {flight.plane_model} \n" + \
                           f"Вылет: {flight.departure_date_time.strftime('%Y-%m-%d %H:%M')} \n" + \
                           f"Прилёт: {flight.arrival_date_time.strftime('%Y-%m-%d %H:%M')} \n" + \
                           f"Время в рейсе: {time_in_flight} \n\n" + \
                           f"Ссылки на трекер: \n{links}"

        self.start = flight.departure_date_time - timedelta(hours=2)
        self.end = flight.arrival_date_time

        start_distance_from_day_begin = self.start - datetime(self.start.year, self.start.month, self.start.day)
        begin_gap = timedelta(seconds=0 * 60 * 60 + 30 * 60)
        end_gap = timedelta(seconds=5 * 60 * 60 + 30 * 60)
        if begin_gap < start_distance_from_day_begin < end_gap:
            self.color = 10
        else:
            self.color = 7

    def __create_reserve(self, reserve: Reserve):
        self.summary = "Резерв"
        self.description = reserve.info
        self.start = reserve.begin_date_time
        self.end = reserve.end_date_time
        self.color = 5

    def __create_work_event(self, event: WorkEvent):
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
