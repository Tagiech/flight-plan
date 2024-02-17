from datetime import timedelta

from configs.config import login, password
from domain.calendar_event import CalendarEvent
from domain.flight import Flight
from domain.reserve import Reserve
from domain.work_event import WorkEvent
from repository.google_calendar_repository import GoogleCalendar
from repository.workplan_repository import WorkPlan
from services.telegram_logger import TelegramLogger


class ActualizeCalendarHandler(object):

    def __init__(self):
        self.__calendar_repository = GoogleCalendar()
        self.__workplan_repository = WorkPlan()
        self.__logger = TelegramLogger()

    def handle(self):
        calendar_events = self.__calendar_repository.get_events_list()
        flights, reserves, work_events = self.__workplan_repository.getPlan(login, password)

        deleted_events_qty = self.__check_for_deleted_flights(calendar_events, flights, reserves, work_events)
        created_events_qty = self.__update_calendar_events(calendar_events, flights, reserves, work_events)

        if created_events_qty + deleted_events_qty > 0:
            self.__logger.log_changes_in_calendar(created_events_qty, deleted_events_qty)

        self.__workplan_repository.close()

    def __update_calendar_events(self,
                                 calendar_events,
                                 flights: list[Flight],
                                 reserves: list[Reserve],
                                 work_events: list[WorkEvent]) -> int:
        events: list[CalendarEvent] = []
        created_events_qty: int = 0

        for flight in flights:
            events.append(CalendarEvent(flight))
        for reserve in reserves:
            events.append(CalendarEvent(reserve))
        for work_event in work_events:
            events.append(CalendarEvent(work_event))

        for event in events:
            if not self.__event_exists(event, calendar_events):
                self.__calendar_repository.create_event(event.toJson())
                created_events_qty += 1
        return created_events_qty

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
                                    work_events: list[WorkEvent]) -> int:
        deleted_events_qty: int = 0
        for calendar_event in calendar_events:
            if self.__flight_exists(calendar_event, flights, reserves, work_events):
                pass
            else:
                self.__calendar_repository.delete_event(calendar_event['id'])
                deleted_events_qty += 1
        return deleted_events_qty

    def __flight_exists(self,
                        calendar_event,
                        flights: list[Flight],
                        reserves: list[Reserve],
                        work_events: list[WorkEvent]) -> bool:
        event_start_datetime = calendar_event['start'].get('dateTime', calendar_event['start'].get('date'))
        event_end_datetime = calendar_event['end'].get('dateTime', calendar_event['end'].get('date'))
        for flight in flights:
            flight_start = (flight.departure_date_time - timedelta(hours=2)).astimezone().isoformat()
            flight_end = flight.arrival_date_time.astimezone().isoformat()
            if event_start_datetime == flight_start and event_end_datetime == flight_end:
                return True
        for reserve in reserves:
            reserve_start = reserve.begin_date_time.astimezone().isoformat()
            reserve_end = reserve.end_date_time.astimezone().isoformat()
            if event_start_datetime == reserve_start and event_end_datetime == reserve_end:
                return True
        for work_event in work_events:
            work_event_start = work_event.begin_date_time.astimezone().isoformat()
            work_event_end = work_event.end_date_time.astimezone().isoformat()
            if event_start_datetime == work_event_start and event_end_datetime == work_event_end:
                return True
        return False
