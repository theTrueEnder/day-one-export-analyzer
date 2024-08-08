from entry import Entry

NO_MATCH_CODE = -1
NO_MATCH_MSG = 'No entries matched filter'
SUCCESS_CODE = 1


class Journal():
    def __init__(self, entries=[]):
        self.entries = entries
        
    def __str__(self):
        ...
        
    def get_entry_count(self):
        return len(self.entries)
        
    def _return_filter_result(filtered_entries):
        e_ct = len(filtered_entries)
        if e_ct == 0:
            return {"code": NO_MATCH_CODE, "msg": NO_MATCH_MSG, "count": 0}
        else:
            return {"code": SUCCESS_CODE, "msg": filtered_entries, "count": e_ct}
            
    def filter_starred(self, starred=True, in_place=False):
        entries = [entry for entry in self.entries if entry.is_starred()]
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self.entries = entries
        return res
        
    def filter_pinned(self, starred=True, in_place=False):
        entries = [entry for entry in self.entries if entry.is_pinned()]
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self.entries = entries
        return res
        
    def filter_by_country(self, country, in_place=False):
        entries = [entry for entry in self.entries if country == entry.get_country()]
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self.entries = entries
        return res
        
    def filter_by_admin_area(self, admin_area, in_place=False):
        entries = [entry for entry in self.entries if admin_area == entry.get_admin_area()]
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self.entries = entries
        return res
        
    def filter_by_locality(self, locality, in_place=False):
        entries = [entry for entry in self.entries if locality == entry.get_locality()]
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self.entries = entries
        return res
        
    def filter_by_placename(self, placename, in_place=False):
        entries = [entry for entry in self.entries if placename == entry.get_placename()]
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self.entries = entries
        return res
        
    def filter_by_tags(self, tags=[], in_place=False):
        entries = ...
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self.entries = entries
        return res
        
    def filter_by_keyword(self, keyword, in_place=False):
        entries = ...
        res = self._return_filter_result(entries)
        if res['code'] == SUCCESS_CODE and in_place:
            self.entries = entries
        return res