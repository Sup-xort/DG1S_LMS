from django.contrib import admin
from .models import *
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from django.utils import timezone

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class StudentAdmin(admin.ModelAdmin):
    search_fields = ['num', 'name']
    list_display = ['num', 'name']

    @admin.action(description="이동현황 초기화")
    def set(self, request, queryset):
        ip_address = get_client_ip(request)
        for student in queryset:
            card = Card(stu=student, to='재실', why='관리자에 의해 초기화되었습니다.', moving_date=timezone.now(), ip=ip_address)
            card.save()
        self.message_user(request, "초기화 되었습니다.")

    actions = [set]

    @admin.action(description="조퇴자 제외 이동현황 초기화")
    def set(self, request, queryset):
        ip_address = get_client_ip(request)
        for student in queryset:
            to = Card.objects.filter(stu=student).order_by('-moving_date').first()

            if to != '조퇴':
                card = Card(stu=student, to='재실', why='관리자에 의해 초기화되었습니다.', moving_date=timezone.now(), ip=ip_address)
                card.save()

        self.message_user(request, "초기화 되었습니다.")

    actions = [set]

class CardAdmin(admin.ModelAdmin):
    search_fields = ['stu__num', 'stu__name', 'to', 'why', 'moving_date', 'ip']
    list_display = ['stu', 'to', 'moving_date', 'ip']
    list_filter = ('to', ('moving_date', DateRangeFilter))

class PreCardAdmin(admin.ModelAdmin):
    search_fields = ['stu__num', 'stu__name', 'time', 'to', 'why', 'moving_date', 'ip']
    list_filter = ('to', 'time', ('moving_date', DateRangeFilter), 'approved')
    list_display = ('get_stus', 'to', 'time', 'approved', 'moving_date', 'pw', 'ip')

    def get_stus(self, obj):
        return ", ".join([stu.name for stu in obj.stus.all()])

    get_stus.short_description = 'Students'

    @admin.action(description="Upload PreCard")
    def Uploade(self, request, queryset):
        ip_address = get_client_ip(request)
        cnt = 0
        for pcard in queryset:
            if pcard.approved == True:
                cnt += 1
                for s in pcard.stus.all():
                    card = Card(stu=s, to=pcard.to, why=pcard.why, moving_date=timezone.now(), ip=ip_address)
                    card.save()
        self.message_user(request, f"{queryset.count()}건중 승인된 {cnt}건의 요청이 이동 현황에 등록됩니다: request Uploaded.")

    @admin.action(description="Approve PreCard")
    def Approve(self, request, queryset):
        ip_address = get_client_ip(request)
        for pcard in queryset:
            pcard.approved = True
            pcard.save()
        self.message_user(request, f"{queryset.count()}건의 이동 요청이 승인되었습니다: request approved.")
    
    actions = [Approve, Uploade]




admin.site.register(Student, StudentAdmin)
admin.site.register(PreCard, PreCardAdmin)
admin.site.register(Card, CardAdmin)
admin.site.index_title = 'DG1S LMS'
admin.site.site_header = 'DG1S LMS Admin'
admin.site.site_title = 'Administration'