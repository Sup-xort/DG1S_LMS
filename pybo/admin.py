from django.contrib import admin
from .models import *

class StudentAdmin(admin.ModelAdmin):
    search_fields = ['num', 'name']

class CardAdmin(admin.ModelAdmin):
    search_fields = ['to', 'why']

class PreCardAdmin(admin.ModelAdmin):
    search_fields = ['time', 'to', 'why']

admin.site.register(Student, StudentAdmin)
admin.site.register(PreCard, PreCardAdmin)
admin.site.register(Card, CardAdmin)

# Register your models here.
