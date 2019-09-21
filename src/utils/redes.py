from subprocess import PIPE, Popen


class Red:
    
    def __str__(self):
        return self.essid
    
    @property
    def essid(self):
        if "essid" in list(self.d.keys()):
            return self.d['essid']
        return None

    @property
    def bssid(self):
        if "bssid" in list(self.d.keys()):
            return self.d['bssid']
        return None
    
    @property
    def channel(self):
        if "channel" in list(self.d.keys()):
            return int(self.d['channel'])
        return None
    
    @property
    def dbm(self):
        if "dbm" in list(self.d.keys()):
            return int(self.d['dbm'])
        return None
    
    @property
    def lock(self):
        if "lock" in list(self.d.keys()):
            return self.d['lock']
        return None
    
    @property
    def vendor(self):
        if "vendor" in list(self.d.keys()):
            return self.d['vendor']
        return None
    
    @property
    def wps(self):
        if "wps" in list(self.d.keys()):
            return float(self.d['wps'])
        return None
    
    @property
    def progress(self):
        if "progress" in list(self.d.keys()):
            try:
                return float(self.d['progress'])
            except Exception as e:
                return float(0.0)
        return None

    @property
    def parser_to_table(self):
        return [
            self.essid, self.bssid, self.channel, self.dbm,
            self.lock, self.vendor, self.wps, f"{self.progress}%"
        ]
    
    @property
    def diccionario(self):
        header_list = ['essid', 'bssid', 'channel', 'dbm', 'lock', 'vendor', 'wps', 'progress']
        valores_list = self.parser_to_table
        junto = zip(header_list, valores_list)
        return dict(junto)

    # ─── LOADER ─────────────────────────────────────────────────────────────────────

    def load_from_lista(self, lista):
        header = ['essid', 'bssid', 'channel', 'dbm', 'lock', 'vendor', 'wps', 'progress']
        junto = zip(header, lista)
        self.d = dict(junto)
    
    def load_from_json(self, data):
        self.d = dict(data)
    
    # ────────────────────────────────────────────────────────────────────────────────
