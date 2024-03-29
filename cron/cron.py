from .models import *
from django.utils import timezone

def load430():
    for card in PreCard.objects.get(moving_date=timezone.now().date, time="8, 9교시"):
        a = Card(stu=card.stu, to_=card.to, why=card.why, moving_date=card.moving_date)
        a.save()

def load620():
    for card in PreCard.objects.get(moving_date=timezone.now().date, time="8, 9교시"):
        a = Card(stu=card.stu, to_=card.to, why=card.why, moving_date=card.moving_date)
        a.save()
def mstatu():
    q = Student.objects.all()
    a = Card(to='재실', why='초기상태', stu=q)
    a.save()