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
        self._tz = e['timeZone'].replace('\\/', '/')
        self._created = convert_to_local(self._tz, e['creationDate'])
        self._edit_duration = timedelta(seconds=e['editingTime'])
        self._completed = self._created + self._edit_duration
        self._uuid = e['uuid']
        if 'location' in e:
            self._lat = e['location']['latitude']
            self._long = e['location']['longitude']

    def get_created_time(self):
        return self._created
        
    def get_completed_time(self):
        return self._completed
    