import azure.functions as func
import logging
from datetime import datetime

from daily_booking import adlogin_book_by_date, get_date

app = func.FunctionApp()

@app.schedule(schedule="30 59 15 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def book(myTimer: func.TimerRequest) -> None:
    logging.basicConfig(level=logging.INFO)
    logging.info('Python timer trigger function ran at UTC--%s', datetime.utcnow())
    date = get_date(d=2, UTC=8)
    rooms = ["Discussion Room", "Study Room"]
    query = {'date': date, 'room': {'$in': rooms}, 'state': {'$in': ['prebooked', 'failed']}}
    adlogin_book_by_date(date, query, time="0000")


@app.schedule(schedule="30 59 15 * * *", arg_name="myTimer", run_on_startup=False,
                use_monitor=False)
def bookCCMorning(myTimer: func.TimerRequest) -> None:
    logging.basicConfig(level=logging.INFO)
    logging.info('Python timer trigger function ran at UTC--%s', datetime.utcnow())
    date = get_date(d=1, UTC=8)
    rooms = ["Concept and Creation Room"]
    query = {'date': date, 'room': {'$in': rooms}, 'state': {'$in': ['prebooked', 'failed']}, "times": '08301300'}
    adlogin_book_by_date(date, query, aday=0, time="0000")


@app.schedule(schedule="30 29 00 * * *", arg_name="myTimer", run_on_startup=False,
                use_monitor=False)
def bookCCAfternoon(myTimer: func.TimerRequest) -> None:
    logging.basicConfig(level=logging.INFO)
    logging.info('Python timer trigger function ran at UTC--%s', datetime.utcnow())
    date = get_date(d=0, UTC=8)
    rooms = ["Concept and Creation Room"]
    query = {'date': date, 'room': {'$in': rooms}, 'state': {'$in': ['prebooked', 'failed']}, "times": '13001800'}
    adlogin_book_by_date(date, query, aday=0, time="0830")


@app.schedule(schedule="30 59 04 * * *", arg_name="myTimer", run_on_startup=False,
                use_monitor=False)
def bookCCNight(myTimer: func.TimerRequest) -> None:
    logging.basicConfig(level=logging.INFO)
    logging.info('Python timer trigger function ran at UTC--%s', datetime.utcnow())
    date = get_date(d=0, UTC=8)
    rooms = ["Concept and Creation Room"]
    query = {'date': date, 'room': {'$in': rooms}, 'state': {'$in': ['prebooked', 'failed']}, "times": '18002200'}
    adlogin_book_by_date(date, query, aday=0, time="1300")