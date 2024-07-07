from django.db import models

# Create your models here.
class Student(models.Model):
    num = models.SmallIntegerField()
    name = models.CharField(max_length=15)

    def __str__(self):
        return (str(self.num)+self.name)

class Card(models.Model):
    stu = models.ForeignKey(Student, on_delete=models.CASCADE)
    to = models.CharField(max_length=40)
    why = models.TextField(null=True, blank=True)
    moving_date = models.DateTimeField()
    ip = models.GenericIPAddressField()

    def __str__(self):
        return (str(self.stu.num)+' '+self.stu.name + '  ' +  self.to)

class PreCard(models.Model):
    stus = models.ManyToManyField(Student)
    to = models.CharField(max_length=40)
    why = models.TextField(null=True, blank=True)
    moving_date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    approved = models.BooleanField(default=False)

    pw = models.SmallIntegerField()

    time = models.CharField(max_length=30)

    def __str__(self):
        return f"{', '.join([stu.name for stu in self.stus.all()])}"