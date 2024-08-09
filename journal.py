from entry import Entry

SUCCESS_CODE = 1
NO_MATCH_CODE = -1
NO_MATCH_MSG = 'No entries matched filter'


class Journal():
    def __init__(self, entries=[]):
        self.uuid_entries = {}
        [self.uuid_entries.update({"uuid": entry.get_uuid(), "entry": entry}) for entry in entries]
        self._update_entries(entries)
        
    def __str__(self)->str:
        s = f'Journal object:\n\t{self.get_entry_count()} entries:\n\t'
        for entry in self.entries:
            s += str(entry)
        return s
        
    def __add__(self, other):
        [self.uuid_entries.update({entry.get_uuid(): entry}) for entry in other.get_entries()]
        self.entries = list(self.uuid_entries.keys())
        return self
        
    def __sub__(self, other):
        [self.uuid_entries.pop(entry.get_uuid(), None) for entry in other.get_entries()]
        self.entries = list(self.uuid_entries.keys())
        return self
        
        
    def _update_entries(self, updated_entries):
        self.uuid_entries.clear()
        [self.uuid_entries.update({entry.get_uuid(): entry}) for entry in updated_entries]
        self.entries = updated_entries
        
    def _return_filter_result(self, filtered_entries: list[Entry]):
        e_ct = len(filtered_entries)
        if e_ct == 0:
            return {"code": NO_MATCH_CODE, "msg": NO_MATCH_MSG, "count": 0}
        else:
            return {"code": SUCCESS_CODE, "msg": filtered_entries, "count": e_ct}
            
            
            
    def get_entry_count(self)->int:
        return len(self.entries)
    
    def get_entries(self)->list[Entry]:
        return self.entries
    
    def filter_starred(self, starred=True, in_place=False)->dict:
        if starred:
            entries = [entry for entry in self.entries if entry.is_starred()]
        else:
            entries = [entry for entry in self.entries if not entry.is_starred()]
    
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self._update_entries(entries)
        return res
        
    def filter_pinned(self, pinned=True, in_place=False)->dict:
        if pinned:
            entries = [entry for entry in self.entries if entry.is_pinned()]
        else:
            entries = [entry for entry in self.entries if not entry.is_pinned()]
            
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self._update_entries(entries)
        return res
        
    def filter_by_country(self, country: str, negative=False, in_place=False)->dict:
        print(f'Finding country: "{country}"')
        if not negative:
            entries = [entry for entry in self.entries if country == entry.get_country()]
        else:
            entries = [entry for entry in self.entries if country == entry.get_country()]
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self._update_entries(entries)
        return res
        
    def filter_by_admin_area(self, admin_area: str, negative=False, in_place=False)->dict:
        if not negative:
            entries = [entry for entry in self.entries if admin_area == entry.get_admin_area()]
        else:
            entries = [entry for entry in self.entries if admin_area != entry.get_admin_area()]
            
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self._update_entries(entries)
        return res
        
    def filter_by_locality(self, locality: str, negative=False, in_place=False)->dict:
        if not negative:
            entries = [entry for entry in self.entries if locality == entry.get_locality()]
        else:
            entries = [entry for entry in self.entries if locality != entry.get_locality()]
            
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self._update_entries(entries)
        return res
        
    def filter_by_placename(self, placename: str, negative=False, in_place=False)->dict:
        if not negative:
            entries = [entry for entry in self.entries if placename == entry.get_placename()]
        else:
            entries = [entry for entry in self.entries if placename != entry.get_placename()]
            
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self._update_entries(entries)
        return res
        
    def filter_by_tags(self, tags=[], negative=False, match_all=False, in_place=False)->dict:
        # if not negative:
        tagset = set(tags)
        entries = []
        for entry in self.entries:
            etagset = set(entry.get_tags())
            if not negative:
                if match_all and tagset.issubset(etagset):
                    entries.append(entry)
                elif not match_all and tagset.issubset(etagset):
                    entries.append(entry) 
            else:
                if match_all and not tagset.issubset(etagset):
                    entries.append(entry)
                elif not match_all and not tagset.issubset(etagset):
                    entries.append(entry) 
            
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self._update_entries(entries)
        return res
        
    def filter_by_keyword(self, keyword: str, negative=False, in_place=False)->dict:
        print(f'Finding {keyword} in entries..')
        if not negative:
            entries = [entry for entry in self.entries if keyword in entry.get_text()]
        else:
            entries = [entry for entry in self.entries if keyword not in entry.get_text()]
            
        print(f'{len(entries)} matching entries found!')
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self._update_entries(entries)
        return res