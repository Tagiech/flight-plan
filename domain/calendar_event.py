from datetime import datetime

from domain.flight import Flight
from domain.reserve import Reserve
from domain.work_event import WorkEvent


class CalendarEvent:
    Summary: str
    Description: str
    Start: datetime
    End: datetime
    Color: int

    def __init__(self, flight: Flight):
        if len(flight.Airports) > 2:
            self.Summary = f"Командировка в {flight.Airports[0]}"
        else:
            self.Summary = f"Полёт в {flight.Airports[0]}"

        time_in_flight = str(flight.ArrivalDateTime - flight.DepartureDateTime)[:-3]

        self.Description = f"Аэропорты: {flight.Airports} \n" + \
                           f"Номера полетов: {flight.FlightNumber} \n" + \
                           f"Самолёт: {flight.PlaneModel} \n" + \
                           f"Вылет: {flight.DepartureDateTime.strftime('%Y-%m-%d %H:%M')} \n" + \
                           f"Прилёт: {flight.ArrivalDateTime.strftime('%Y-%m-%d %H:%M')} \n" + \
                           f"Время в рейсе: {time_in_flight}"

        self.Start = flight.DepartureDateTime - datetime.timedelta(hours=2)
        self.End = flight.ArrivalDateTime

        self.Color = 7

    def __init__(self, reserve: Reserve):
        self.Summary = "Резерв"
        self.Description = reserve.Info
        self.Start = reserve.BeginDateTime
        self.End = reserve.EndDateTime
        self.Color = 5

    def __init__(self, event: WorkEvent):
        self.Summary = event.Info
        self.Description = ""
        self.Start = event.BeginDateTime
        self.End = event.EndDateTime
        self.Color = 3

    def toJson(self):
        return {
            'summary': self.Summary,
            'description': self.Description,
            'colorId': str(self.Color),
            'start': {
                'dateTime': self.Start.astimezone().isoformat(),
            },
            'end': {
                'dateTime': self.End.astimezone().isoformat(),
            }
        }
