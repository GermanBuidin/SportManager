from sport_items.celery import app

from .utils import DayAnalytic, WeekAnalytic, MonthAnalytic



@app.task
def day_analytic():
    analytic = DayAnalytic()
    analytic.make_data()


@app.task
def week_analytic():
    analytic = WeekAnalytic()
    analytic.make_data()


@app.task
def month_analytic():
    analytic = MonthAnalytic()
    analytic.make_data()
