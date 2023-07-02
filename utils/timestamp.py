import datetime


def create_timestamp():
    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y %H:%M:%S")

    return timestamp