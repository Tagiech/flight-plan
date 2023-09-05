from datetime import datetime


class WorkEvent:
    begin_date_time: datetime
    end_date_time: datetime
    info: str

    def __init__(self,
                 begin_date_time: datetime,
                 end_date_time: datetime,
                 info: str):
        self.info = info
        self.begin_date_time = begin_date_time
        self.end_date_time = end_date_time
