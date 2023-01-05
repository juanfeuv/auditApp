from datetime import date
from datetime import datetime

def parseToDate(date: date):
    return datetime.combine(date, datetime.min.time())