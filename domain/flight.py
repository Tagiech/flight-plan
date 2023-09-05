from datetime import datetime


class Flight:
    departure_date_time: datetime
    arrival_date_time: datetime
    flight_number: str
    plane_model: str
    airports: list[str]

    def __init__(self,
                 departure_date_time: datetime,
                 arrival_date_time: datetime,
                 flight_number: str,
                 plane_model: str,
                 airports: list[str]):
        self.departure_date_time = departure_date_time
        self.arrival_date_time = arrival_date_time
        self.flight_number = flight_number
        self.plane_model = plane_model
        self.airports = airports
