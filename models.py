from peewee import *

DATABASE = PostgresqlDatabase(
    'flask_social',
)


class PeopleServed(Model):
    date = DateField()
    people = IntegerField()

    class Meta:
        database = DATABASE
        order_by = ('-date',)


def initialise():
    DATABASE.get_conn()
    DATABASE.create_tables([PeopleServed], safe=True)
    DATABASE.close()