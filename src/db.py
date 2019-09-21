import peewee
import datetime

db = peewee.SqliteDatabase('database.db')


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
        db.create_tables([RedDB])
    except Exception as e:
        print(e)
        print("error!")
    