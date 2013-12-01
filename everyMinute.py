from sched import scheduler
from time import time, sleep
from summonBot import main as runBot

s = scheduler(time, sleep)

def run_periodically(start, end, interval, func):
    event_time = start
    while event_time < end:
        s.enterabs(event_time, 0, func, ())
        event_time += interval
    s.run()

if __name__ == '__main__':
    run_periodically(time()+1, time()+86400, 30, runBot)
