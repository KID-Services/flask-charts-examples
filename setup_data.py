import datetime
import random
import models
 

def daterange(start_date, end_date):
    if start_date <= end_date:
        for n in range((end_date - start_date).days + 1):
            yield start_date + datetime.timedelta(n)
    else:
        for n in range((start_date - end_date).days + 1):
            yield start_date - datetime.timedelta(n)


def create_data():
    # Delete all people served
    models.PeopleServed.delete().execute()

    start = datetime.date(year=2015, month=2, day=1)
    end = datetime.date(year=2017, month=1, day=1)

    for date in daterange(start, end):
        models.PeopleServed.create(
            date=date,
            people=random.randrange(0, 150)
        )


if __name__ == '__main__':
    models.initialise()
    create_data()
