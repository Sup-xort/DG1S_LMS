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
    stu = models.ForeignKey(Student, on_delete=models.CASCADE)
    to = models.CharField(max_length=40)
    why = models.TextField(null=True, blank=True)
    moving_date = models.DateTimeField()
    ip = models.GenericIPAddressField()

    category = (('1차야자', '1차야자'), ('8, 9교시', '8, 9교시'))
    time = models.CharField(max_length=20, choices=category)
    def __str__(self):
        return (str(self.stu.num)+self.stu.name + '  ' +  self.to)