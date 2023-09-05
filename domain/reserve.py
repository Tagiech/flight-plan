from datetime import datetime

class Reserve:
    BeginDateTime: datetime
    EndDateTime: datetime
    Info: str

    def __init__(self,
                 beginDateTime: datetime,
                 endDateTime: datetime,
                 info: str):
        self.Info = info
        self.BeginDateTime = beginDateTime
        self.EndDateTime = endDateTime
