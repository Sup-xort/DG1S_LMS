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
    path('quick/<int:stu_num>', views.Quick, name='Quick'),
    path('quick/search', views.toQuick, name='toQuick'),
    path('table/', views.table, name='table'),
    path('toolbox/', views.toolbox, name='toolbox'),
    path('hmltolatex/', views.hmltolatex, name='hmltolatex'),
    path('conv/', views.conv, name='conv'),
    path('neis/', views.neis, name='neis'),
    path('check_spelling/', views.check_spelling, name='check_spelling'),
    path('status_board/', views.status_board, name='status_board'),
    path('setset/', views.reset, name='reset'),
    path('precard/view', views.view_precard, name='view_precard'),
    path('precard/password/<int:pcard_id>/<int:task>', views.password, name='password'),
    path('precard/create/name/', views.name, name='name'),
    path('precard/create/form/', views.PreCard_create_many, name='PreCard_create_many'),
    path('precard/rewrite/name/', views.name_re, name='name_re'),
    path('precard/rewrite/form/', views.PreCard_create_many_re, name='PreCard_create_many_re'),
]
