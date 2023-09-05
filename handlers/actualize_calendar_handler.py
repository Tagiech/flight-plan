from datetime import timedelta

from configs.config import login, password
from domain.calendar_event import CalendarEvent
from domain.flight import Flight
from domain.reserve import Reserve
from domain.work_event import WorkEvent
from repository.google_calendar_repository import GoogleCalendar
from repository.workplan_repository import WorkPlan


class ActualizeCalendarHandler(object):

    def __init__(self):
        self._calendar_repository = GoogleCalendar()
        self._workplan_repository = WorkPlan()

    def handle(self):
        calendar_events = self._calendar_repository.get_events_list()
        flights, reserves, work_events = self._workplan_repository.getPlan(login, password)

        self.__check_for_deleted_flights(calendar_events, flights, reserves, work_events)
        self.__update_calendar_events(calendar_events, flights, reserves, work_events)

    def __update_calendar_events(self,
                                 calendar_events,
                                 flights: list[Flight],
                                 reserves: list[Reserve],
                                 work_events: list[WorkEvent]):
        events = []

        for flight in flights:
            events.append(CalendarEvent(flight))
        for reserve in reserves:
            events.append(CalendarEvent(reserve))
        for work_event in work_events:
            events.append(CalendarEvent(work_event))

        for event in events:
            if not self.__event_exists(event, calendar_events):
                self._calendar_repository.create_event(event.toJson())

    def __event_exists(self,
                       event: CalendarEvent,
                       calendar_events) -> bool:
        for calendar_event in calendar_events:
            calendar_start = calendar_event['start']['dateTime']
            calendar_end = calendar_event['end']['dateTime']
            if (event.start.astimezone().isoformat() == calendar_start
                    and event.end.astimezone().isoformat() == calendar_end):
                return True
        return False

    def __check_for_deleted_flights(self,
                                    calendar_events,
                                    flights: list[Flight],
                                    reserves: list[Reserve],
                                    work_events: list[WorkEvent]):
        for calendar_event in calendar_events:
            if self.__flight_exists(calendar_event, flights, reserves, work_events):
                pass
            else:
                self._calendar_repository.delete_event(calendar_event['id'])

    def __flight_exists(self,
                        calendar_event,
                        flights: list[Flight],
                        reserves: list[Reserve],
                        work_events: list[WorkEvent]) -> bool:
        event_start_datetime = calendar_event['start'].get('dateTime', calendar_event['start'].get('date'))
        for flight in flights:
            flight_start = (flight.departure_date_time - timedelta(hours=2)).astimezone().isoformat()
            if event_start_datetime == flight_start:
                return True
        for reserve in reserves:
            reserve_start = reserve.begin_date_time.astimezone().isoformat()
            if event_start_datetime == reserve_start:
                return True
        for work_event in work_events:
            work_event_start = work_event.begin_date_time.astimezone().isoformat()
            if event_start_datetime == work_event_start:
                return True
        return False
