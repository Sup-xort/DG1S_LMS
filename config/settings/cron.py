from pybo.models import *
from django.utils import timezone

def load430():
    for card in PreCard.objects.filter(moving_date__date=timezone.now().date(), time="8, 9교시"):
        a = Card(stu=card.stu, to_=card.to, why=card.why, moving_date=card.moving_date)
        a.save()

def load620():
    for card in PreCard.objects.filter(moving_date__date=timezone.now().date(), time="1차야자"):
        a = Card(stu=card.stu, to_=card.to, why=card.why, moving_date=card.moving_date)
        a.save()
def mstatu():
    students = Student.objects.all()
    for student in students:
        a = Card(to='재실', why='초기상태', stu=student, moving_date=timezone.now())
        a.save()