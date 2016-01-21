from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from enums import Periodicidad


class SchedulerManager():
    def __init__(self, perfiles):
        self.scheduler = BackgroundScheduler()
        for perfil in perfiles:
            self.add_job(perfil)

    def start(self):
        self.scheduler.start()

    def add_job(self, perfil):

        if perfil.periodicidad == Periodicidad.diaria.value:
            self.scheduler.add_job(send_mail, 'interval', id=perfil.user_id, replace_existing=True, days=1,
                                   start_date=today_date())

        elif perfil.periodicidad == Periodicidad.semanal.value:
            self.scheduler.add_job(send_mail, 'interval', id=perfil.user_id, replace_existing=True, weeks=1,
                                   start_date=today_date())

        elif perfil.periodicidad == Periodicidad.mensual.value:
            self.scheduler.add_job(send_monthly_mail, 'interval', id=perfil.user_id, replace_existing=True, days=1,
                                   start_date=today_date())

    def stop_all(self):
        self.scheduler.shutdown()


def today_date():
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def send_mail():
    print("mail nuevo ")


def send_monthly_mail():
    if datetime.now().day == 1:
        send_mail()
