import peewee


db = peewee.SqliteDatabase('database.db')

# ─── CONFIGURACIONES ────────────────────────────────────────────────────────────

class ReaverConfig(peewee.Model):

    name = peewee.CharField(unique=True)
    delay = peewee.BooleanField(default=False)
    delay_value = peewee.CharField(default="")
    pin = peewee.BooleanField(default=False)
    pin_value = peewee.CharField(default="")
    recurring = peewee.BooleanField(default=False)
    recurring_value = peewee.CharField(default="")
    timeout = peewee.BooleanField(default=False)
    timeout_value = peewee.CharField(default="")
    timeout_m57 = peewee.BooleanField(default=False)
    timeout_m57_value = peewee.CharField(default="")
    ignore_fcs = peewee.BooleanField(default=False)
    ignore_fcs_value = peewee.CharField(default="")
    noassociate = peewee.BooleanField(default=False)
    noassociate_value = peewee.CharField(default="")
    nonack = peewee.BooleanField(default=False)
    nonack_value = peewee.CharField(default="")
    pixie = peewee.BooleanField(default=False)
    pixie_value = peewee.CharField(default="")
    verbose = peewee.IntegerField(default=0)

    class Meta:
        database = db
        db_table = 'reaver_configs'
    
    def update_info(self, data):
        self._update_bools(data)
        self._update_values(data)
        self.verbose = data['verbose'][1]

    def _update_bools(self, data):
        self.delay = data['delay'][0]
        self.pin = data['pin'][0]
        self.recurring = data['recurring'][0]
        self.timeout = data['timeout'][0]
        self.timeout_m57 = data['timeout_m57'][0]
        self.ignore_fcs = data['ignore_fcs'][0]
        self.noassociate = data['noassociate'][0]
        self.nonack = data['nonack'][0]
        self.pixie = data['pixie'][0]
    
    def _update_values(self, data):
        self.delay_value = data['delay'][1]
        self.pin_value = data['pin'][1]
        self.recurring_value = data['recurring'][1]
        self.timeout_value = data['timeout'][1]
        self.timeout_m57_value = data['timeout_m57'][1]

# ────────────────────────────────────────────────────────────────────────────────


# ─── REDES ──────────────────────────────────────────────────────────────────────

class RedDB(peewee.Model):

    bssid = peewee.CharField(unique=True)
    essid = peewee.CharField(default="")
    notas = peewee.TextField(default="")

    class Meta:
        database = db
        db_table = 'redes'


#
if __name__ == '__main__':
    try:
        db.connect()
        db.create_tables([RedDB, ReaverConfig])
    except Exception as e:
        print(e)
        print("error!")
    