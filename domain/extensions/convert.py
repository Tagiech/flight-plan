from datetime import datetime

from bs4 import BeautifulSoup

from domain.flight import Flight
from domain.reserve import Reserve
from domain.work_event import WorkEvent


def to_flight(html: BeautifulSoup) -> list[Flight]:
    flights = []
    for row in html.find_all('tr'):
        spans = row.find_all('span')
        try:
            if spans[0]['class'][0] == 'plan_del':
                continue
        except KeyError:
            pass
        departure_datetime = datetime.strptime(spans[0].text + ' ' + spans[1].text, '%d.%m.%Y %H:%M')
        route = spans[5].text.split('     ')[0].strip().replace('ПУЛКОВО-1 / ', '').split(' / ')
        airports = []
        for airport in route:
            airports.append(airport[:1] + airport[1:].lower())
        arrival_datetime = datetime.strptime(spans[5].text.split('[прил. ')[1][:16], '%d.%m.%Y %H:%M')
        flight_number = spans[3].text.replace('ФВ', 'FV')
        plane_model = spans[4].text
        flights.append(
            Flight(departure_datetime, arrival_datetime, flight_number, plane_model, airports))

    return flights


def to_reserve(html: BeautifulSoup) -> list[Reserve]:
    reserves = []
    for row in html.find_all('tr'):
        tds = row.find_all('td')
        begin_datetime = datetime.strptime(tds[0].text, '%d.%m.%Y %H:%M')
        info = tds[1].text.replace('\xa0\n\t\t\t\t\t\t\t\t\t\t', ' ').split('[до ')[0].strip()
        end_datetime = datetime.strptime(tds[1].text.replace('\xa0\n\t\t\t\t\t\t\t\t\t\t', ' ').split('[до ')[1][:16],
                                         '%d.%m.%Y %H:%M')
        reserves.append(Reserve(begin_datetime, end_datetime, info))

    return reserves


def to_work_event(html: BeautifulSoup) -> list[WorkEvent]:
    events = []
    for row in html.find_all('tr'):
        spans = row.find_all('span')
        begin_datetime = datetime.strptime(spans[0].text + ' ' + spans[1].text, '%d.%m.%Y %H:%M')
        info = spans[2].text
        end_datetime = datetime.strptime(spans[4].text.split('[до ')[1][:16], '%d.%m.%Y %H:%M')
        events.append(WorkEvent(begin_datetime, end_datetime, info))

    return events
