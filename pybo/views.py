from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import *
from .forms import *
from .crolling import meal

def home(request):
    dish = meal()
    context = {'b': dish[0], 'l': dish[1], 'd': dish[2]}

    return render(request, 'pybo/home.html', context)

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    stu_list = Student.objects.order_by('num')
    paginator = Paginator(stu_list, 20)
    page_obj = paginator.get_page(page)
    context = {'stu_list': page_obj}
    return render(request, 'pybo/student_list.html', context)

def event(request):
    page = request.GET.get('page', '1')  # 페이지
    card_list = Card.objects.order_by('-moving_date')
    paginator = Paginator(card_list, 40)
    page_obj = paginator.get_page(page)
    context = {'card_list': page_obj}
    return render(request, 'pybo/event_list.html', context)

def detail(request, stu_id):
    page = request.GET.get('page', '1')
    stu = Student.objects.get(id=stu_id)
    card = stu.card_set.order_by('-moving_date')

    paginator = Paginator(card, 10)
    page_obj = paginator.get_page(page)
    context = {'student': stu, 'card': page_obj}
    return render(request, 'pybo/student_detail.html', context)

def Card_create(request, stu_id):
    student = get_object_or_404(Student, pk=stu_id)
    student.card_set.create(to=request.GET.get('loc'), why='', moving_date=timezone.now())
    return redirect('pybo:detail', stu_id=student.id)

def PreCard_create(request, stu_id):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.to = "특별실(" + str(card.to) + ")"
            card.stu = Student.objects.get(id=stu_id)
            card.moving_date = timezone.now()
            card.save()
            return redirect('pybo:index')
    else:
        form = CardForm()
    return render(request, 'pybo/question_form.html', {'form': form, 'stu_id': stu_id})

def toQuick(request):
    num = request.POST.get('num')
    stu = Student.objects.filter(num=num).first()
    return render(request, 'pybo/quick.html', {'student': stu})

def Quick(request, stu_num):
    stu = Student.objects.filter(num=stu_num).first()
    return render(request, 'pybo/quick.html', {'student': stu})

def table(request):
    return render(request, 'pybo/TABLE.html')