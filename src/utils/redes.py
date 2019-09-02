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
            return float(self.d['progress'])
        return None

    # @property
    # def parser_to_table(self):
    #     return [
    #         self.d['essid'], self.d['bssid'], self.d['channel'],
    #         self.d['dbm'], self.d['lock'], self.d['vendor'],
    #         self.d['wps'], self.d['progress']
    #     ]
    @property
    def parser_to_table(self):
        return [
            self.essid, self.bssid, self.channel, self.dbm,
            self.lock, self.vendor, self.wps, self.progress
        ]
       
    def load_from_lista(self, lista):
        header = ['essid', 'bssid', 'channel', 'dbm', 'lock', 'vendor', 'wps', 'progress']
        junto = zip(header, lista)
        self.d = dict(junto)
    
    def load_from_json(self, data):
        self.d = dict(data)
    
    # def print_self(self):
    #     print(self.__dir__())
    
    # def run_reaver(self, opciones, iface="wlan0mon"):
    #     cmd = "konsole --hold --hide-menubar -e 'reaver -b %s -e %s -c %s %s -i %s'" % (
    #         self.bssid, self.essid, str(self.channel), opciones, iface
    #     )
    #     print(cmd)
    #     proc = Popen(cmd, shell=True)