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
        self._tz = e.get('timeZone').replace('\\/', '/')
        self._created = convert_to_local(self._tz, e.get('creationDate'))
        self._edit_duration = timedelta(seconds=e.get('editingTime'))
        self._completed = self._created + self._edit_duration
        self._uuid = e.get('uuid')
        self._pinned = e.get('isPinned')
        self._starred = e.get('starred')
        self._text = e.get('text')
        self._rich_text = e.get('richText')
        self._country = self._get_multi(e, 'location', 'country')
        self._admin_area = self._get_multi(e, 'location', 'administrativeArea')
        self._locality = self._get_multi(e, 'location', 'localityName')
        self._lat = self._get_multi(e, 'location', 'latitude')
        self._long = self._get_multi(e, 'location', 'longitude')
        self._placename = self._get_multi(e, 'location', 'placeName')
    
    def _get_multi(self, d, *keys):
        val = d.get(keys[0])
        for key in keys:
            if val is None:
                break
            val = val.get(key)
        return val
    
    def get_created_time(self):
        return self._created
        
    def get_completed_time(self):
        return self._completed
    
    def is_starred(self):
        return self._starred
        
    def is_pinned(self):
        return self._pinned
    
    def get_text(self):
        ...
        
    def get_rich_text(self):
        ...
        
    def get_coordinates(self):
        return (self._lat, self._long)
    
    def get_country(self):
        return self._country
    
    def get_admin_area(self):
        return self._admin_area    
        
    def get_locality(self):
        return self._locality
    
    def get_placename(self):
        return self._placename