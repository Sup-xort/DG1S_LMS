from pybo.models import *
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/seoul'})

def load430():
    for card in PreCard.objects.filter(moving_date__date=timezone.now().date(), time="8, 9교시"):
        PreCard.objects.create(stu=card.stu, to_=card.to, why=card.why, moving_date=card.moving_date)

def load620():
    for card in PreCard.objects.filter(moving_date__date=timezone.now().date(), time="1차야자"):
        PreCard.objects.create(stu=card.stu, to_=card.to, why=card.why, moving_date=card.moving_date

def mstatu():
    students = Student.objects.all()
    for student in students:
        Card.objects.create(to='재실', why='초기상태', stu=student, moving_date=timezone.now())

scheduler.add_job(load430, 'cron', day_of_week='mon-fri', hour=16, minute=30)
scheduler.add_job(load620, 'cron', day_of_week='mon-fri', hour=18, minute=30)
scheduler.add_job(mstatu, 'cron', day_of_week='mon-fri', hour=0, minute=0)
scheduler.add_job(mstatu, 'cron', hour=22, minute=17)
