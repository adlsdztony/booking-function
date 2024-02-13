import datetime
import threading
from time import sleep

from db import log
from req import Booker
from TaskClass import createTask

import logging


def get_date(d=0, UTC=0):
    next = datetime.datetime.utcnow() + datetime.timedelta(days=d) + datetime.timedelta(hours=UTC)
    return next.strftime('%Y-%m-%d')

def adlogin_book_with_feedback(task, sleeptime=0.1):
    try:
        t = Booker(task.GetUser(), task)
        t.login()
        while get_date(d=1, UTC=8) != task['date']:
            sleep(sleeptime)
        feedback = t.book()
        if feedback:
            task.ChangeState('booked')
        else:
            task.ChangeState('failed')
    except Exception as e:
        logging.error(e)
        task.ChangeState('failed')


def adlogin_book_by_date(date):
    taskss = log.find({'date': date, '$or': [{'state': 'prebooked'}, {'state': 'failed'}]})

    tasklist = sorted(list(taskss), key=lambda x: x['username'])

    logging.info(f'adlogin_book_by_date: {date}, {len(tasklist)} tasks')

    if len(tasklist) == 0:
        return

    log.delete_many({'date': date, '$or': [{'state': 'prebooked'}, {'state': 'failed'}]})

    # conbine the time of the task from same username
    n = 0
    for t in range(1, len(tasklist)):
        t -= n
        if tasklist[t]['username'] == tasklist[t - 1]['username'] and tasklist[t]['room'] == tasklist[t - 1]['room']:
            tasklist[t - 1]['times'] += tasklist[t]['times']
            del tasklist[t]
            n += 1

    log.insert_many(tasklist)

    thread_list = []
    for i in tasklist:
        logging.info(f'adlogin_book_by_date: Creating task for {i["username"]}')
        i = createTask(i)
        thread_list.append(threading.Thread(target=adlogin_book_with_feedback, args=(i,)))
    for t in thread_list:
        t.start()
        


def book_with_feedback(task):
    try:
        t = Booker(task.GetUser(), task)
        feedback = t.book()
        if feedback:
            task.ChangeState('booked')
        else:
            task.ChangeState('failed')
    except:
        task.ChangeState('failed')


def book_by_date(date):
    tasklist = log.find({'date': date, '$or': [{'state': 'prebooked'}, {'state': 'failed'}]})
    thread_list = []
    for i in tasklist:
        i = createTask(i)
        thread_list.append(threading.Thread(target=book_with_feedback, args=(i,)))
    for t in thread_list:
        t.start()


def book_by_book_date(book_date):
    tasklist = log.find({'book_date': book_date, '$or': [{'state': 'prebooked'}, {'state': 'failed'}]})
    thread_list = []
    for i in tasklist:
        i = createTask(i)
        thread_list.append(threading.Thread(target=book_with_feedback, args=(i,)))
    for t in thread_list:
        t.start()


if __name__ == '__main__':

    adlogin_book_by_date(get_date(d=2, UTC=8))