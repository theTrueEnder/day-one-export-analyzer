from datetime import datetime, timedelta
import pytz

def convert_to_local(tz: str, timestr: str)->datetime:
    utc_time = datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%SZ")
    timezone = pytz.timezone(tz)
    
    # Convert UTC time to the local time of the specified timezone
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(timezone)
    return local_time


class Entry():
    def __init__(self, e: dict):
        self._tz = e.get('timeZone').replace('\\/', '/')
        self._created = convert_to_local(self._tz, e.get('creationDate'))
        self._edit_duration = timedelta(seconds=e.get('editingTime'))
        self._completed = self._created + self._edit_duration
        self._uuid = e.get('uuid')
        self._pinned = e.get('isPinned', False)
        self._starred = e.get('starred', False)
        self._tags = e.get('tags', [])
        self._text = e.get('text', '')
        self._rich_text = e.get('richText', '')
        
        
        self._country = self._get_nested(e, 'location', 'country')
        self._admin_area = self._get_nested(e, 'location', 'administrativeArea')
        self._locality = self._get_nested(e, 'location', 'localityName')
        self._lat = self._get_nested(e, 'location', 'latitude')
        self._long = self._get_nested(e, 'location', 'longitude')
        self._placename = self._get_nested(e, 'location', 'placeName')
    
    def __str__(self)->str:
        s = 'Entry object:\n\t'
        s += f'- UUID: {self._uuid}\n\t'
        s += f'- Created: {self._created}\n\t'
        s += f'- Pinned: {self._pinned}\n\t'
        s += f'- Starred: {self._starred}\n\t'
        s += f'- Tags: {self._tags}\n\t'
        if len(self._text > 10):
            s += f'- Text: "{self._text[:10]}..."\n\t'
        else:
            s += f'- Text: "{self._text}"\n\t'
    
    def _get_nested(self, d: dict, key1, key2, default=None)->any:
        res1 = d.get(key1)
        if res1 is None:
            return None
        else:
            res2 = res1.get(key2)
            return res2
    
    def get_created_time(self)->datetime:
        return self._created
        
    def get_completed_time(self)->datetime:
        return self._completed
    
    def is_starred(self)->bool:
        return self._starred
        
    def is_pinned(self)->bool:
        return self._pinned
        
    def get_coordinates(self)->tuple[float, float]:
        return (self._lat, self._long)
    
    def get_country(self)->str:
        return self._country
    
    def get_admin_area(self)->str:
        return self._admin_area    
        
    def get_locality(self)->str:
        return self._locality
    
    def get_placename(self)->str:
        return self._placename
    
    def get_tags(self)->list[str]:
        return self._tags
    
    def get_text(self)->str:
        return self._text
    
    def get_rich_text(self)->str:
        return self._rich_text
    
    def get_uuid(self)->str:
        return self._uuid