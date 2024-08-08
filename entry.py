from datetime import datetime, timedelta
import pytz

def convert_to_local(tz, timestr):
    utc_time = datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%SZ")
    timezone = pytz.timezone(tz)
    
    # Convert UTC time to the local time of the specified timezone
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)
    return local_time


class Entry():
    def __init__(self, e):
        self.tz = e['timeZone'].replace('\\/', '/')
        self.created = convert_to_local(self.tz, e['creationDate'])
        self.edit_duration = timedelta(seconds=e['editingTime'])
        self.completed = self.created + self.edit_duration
        self.uuid = e['uuid']
        if 'location' in e:
            self.lat = e['location']['latitude']
            self.long = e['location']['longitude']
        
    def get_completed_time(self):
        return self.created