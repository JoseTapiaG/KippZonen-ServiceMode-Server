from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from kippzonenserver.enums import Periodicidad
from kippzonenserver.mail import send_csv
from kippzonenserver.messages import title_mail
from kippzonenserver.models import Registro


class SchedulerManager():
    def __init__(self, perfiles):
        self.scheduler = BackgroundScheduler()
        for perfil in perfiles:
            self.add_job(perfil)

    def start(self):
        self.scheduler.start()

    def add_job(self, perfil):

        if perfil.periodicidad == Periodicidad.diaria.value:
            self.scheduler.add_job(send_mail(Periodicidad.diaria, perfil.user.email), 'interval', id=perfil.user_id, replace_existing=True, days=1,
                                   start_date=today_init_time())

        elif perfil.periodicidad == Periodicidad.semanal.value:
            self.scheduler.add_job(send_mail(Periodicidad.semanal, perfil.user.email), 'interval', id=perfil.user_id, replace_existing=True, weeks=1,
                                   start_date=today_init_time())

        elif perfil.periodicidad == Periodicidad.mensual.value:
            self.scheduler.add_job(send_mail(Periodicidad.mensual, perfil.user.email), 'interval', id=perfil.user_id, replace_existing=True, days=1,
                                   start_date=today_init_time())

    def stop_all(self):
        self.scheduler.shutdown()


def send_mail(periodicity, mail):
    def send_daily():
        date_ini = format_date(today_init_time() + timedelta(days=-1))
        date_end = format_date(today_end_time() + timedelta(days=-1))
        data = get_data(date_ini, date_end)
        title = title_mail.format(date_ini, date_end)
        send_csv(title, data, mail)

    def send_weekly():
        date_ini = format_date(today_init_time() + timedelta(weeks=-1))
        date_end = format_date(today_end_time() + timedelta(days=-1))
        data = get_data(date_ini, date_end)
        title = title_mail.format(date_ini, date_end)
        send_csv(title, data, mail)

    def send_monthly():
        if datetime.now().day == 1:
            date_ini = format_date(first_day_of_month(today_init_time() + timedelta(days=-1)))
            date_end = format_date(today_end_time() + timedelta(days=-1))
            data = get_data(date_ini, date_end)
            title = title_mail.format(date_ini, date_end)
            send_csv(title, data, mail)

    if periodicity == Periodicidad.diaria:
        return send_daily
    elif periodicity == Periodicidad.semanal:
        return send_weekly
    elif periodicity == Periodicidad.mensual:
        return send_monthly


def today_init_time():
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def today_end_time():
    return datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)


def get_data(date_ini, date_end):
    registros = Registro.query.filter(Registro.fecha.between(date_ini, date_end))
    csv_str = ""
    for registro in registros:
        csv_str += registro.fecha.strftime("%Y-%m-%d") + "," + str(registro.dato1) + "," + str(
                registro.dato2) + "," + str(registro.dato3) + "\n"
    return csv_str


def format_date(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")


def first_day_of_month(date):
    return date.replace(day=1)
