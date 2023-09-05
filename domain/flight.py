import datetime


class Flight:
    DepartureDateTime: datetime
    ArrivalDateTime: datetime
    FlightNumber: str
    PlaneModel: str
    Airports: list[str]

    def __init__(self,
                 departureDateTime: datetime,
                 arrivalDateTime: datetime,
                 flightNumber: str,
                 planeModel: str,
                 airports: list[str]):
        self.DepartureDateTime = departureDateTime
        self.ArrivalDateTime = arrivalDateTime
        self.FlightNumber = flightNumber
        self.PlaneModel = planeModel
        self.Airports = airports
