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
    adlogin_book_by_date(get_date(d=2, UTC=8))