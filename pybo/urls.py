from django.urls import path, re_path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('home/<str:day>/', views.hhome, name='hhome'),
    path('index/', views.index, name='index'),
    path('event/', views.event, name='event'),
    path('<int:stu_id>/', views.detail, name='detail'),
    path('card/create/<int:stu_id>/', views.Card_create, name='card_create'),
    path('precard/create/<int:stu_id>/', views.PreCard_create, name='PreCard_create'),
    path('quick/<int:stu_num>', views.Quick, name='Quick'),
    path('quick/search', views.toQuick, name='toQuick'),
    path('table/', views.table, name='table'),
    path('toolbox/', views.toolbox, name='toolbox'),
    path('hmltolatex/', views.hmltolatex, name='hmltolatex'),
    path('conv/', views.conv, name='conv'),
    path('neis/', views.neis, name='neis'),
    path('precard/create/many/<str:l>/', views.name, name='name'),
    path('precard/form/<str:l>/', views.PreCard_create_many, name='PreCard_create_many'),
    path('check_spelling', views.check_spelling, name='check_spelling'),
]
