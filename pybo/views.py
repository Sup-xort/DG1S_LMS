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

def page_not_found(request, exception):
    return render(request, 'pybo/404.html', {})

def server_error(request, exception):
    return render(request, 'pybo/500.html', {})

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
    batch = [[2115, 2114, 2113, 2112, 2111, 2110, 2109, 2108, 2107, 2106, 2105, 2104, 2103, 2102, 2101],
             [0000, 0000, 2116, 2117, 2118, 2119, 2120, 2201, 2202, 2203, 2204, 2205, 2206, 2207, 2208],
             [0000, 0000, 2301, 2220, 2219, 2218, 2217, 2216, 2215, 2214, 2213, 2212, 2211, 2210, 2209],
             [0000, 0000, 0000, 2302, 2303, 2304, 2305, 2306, 2307, 2308, 2309, 2310, 2311, 2312, 2313],
             [0000, 0000, 0000, 2405, 2404, 2403, 2402, 2401, 2320, 2319, 2318, 2317, 2316, 2315, 2314],
             [2406, 2407, 2408, 2409, 2410, 2411, 2412, 2413, 2414, 2415, 2416, 2417, 2418, 2419, 2420]]

    bat = []
    for i in range(0, 6):
        bat.append([])
        for j in range(0, 15):
            if batch[i][j] != 0:
                s = Student.objects.get(num=batch[i][j])
                to = Card.objects.filter(stu=s).order_by('-moving_date').first()
                if to == None:
                    color = '#e0dede'
                    to = ''
                elif '화장실' == to.to:
                    color = '#ffb056'
                    to = to.to
                elif '장탁이용중' == to.to:
                    color = '#569fff'
                    to = to.to
                elif '특별실' == to.to:
                    color = '#af6ef3'
                    to = to.to[3:]
                else:
                    color = '#e0dede'
                    to = ''

                bat[i].append([batch[i][j], s.name, color, to])
            else:
                bat[i].append([0])
    return render(request, 'pybo/TABLE.html', {'stu': Student.objects, 'batch': bat})