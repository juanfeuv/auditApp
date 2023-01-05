import datetime

def parseDate(date: str):
    m, d, y = date.split("/")

    return datetime.datetime(int(y), int(m), int(d))
