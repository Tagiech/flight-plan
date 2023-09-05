import datetime
import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
from configs import config


class GoogleCalendar(object):

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(config.SERVICE_ACCOUNT_FILE,
                                                                            scopes=config.SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    def create_event(self, event):
        (self
         .service
         .events()
         .insert(calendarId=config.calendarId,
                 body=event)
         .execute())

    def get_events_list(self):
        start = datetime.datetime.fromordinal(datetime.date.today().replace(day=1).toordinal()).astimezone().isoformat()
        events_result = self.service.events().list(calendarId=config.calendarId,
                                                   singleEvents=True,
                                                   timeMin=start,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])
