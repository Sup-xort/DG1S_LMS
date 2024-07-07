from django.http import JsonResponse
# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from .models import *
from .forms import *
from .crolling import meal
from pybo.hml_equation_parser import hmlParser as hp
from django.http import JsonResponse
import requests
import json
import time

def home(request):
    return hhome(request, 0)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # X-Forwarded-For 헤더는 쉼표로 구분된 IP 목록을 포함할 수 있습니다.
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hhome(request, day):
    dish = meal(int(day))
    context = {'b': dish[0], 'l': dish[1], 'd': dish[2], 't':dish[3], 'day':day}

    return render(request, 'pybo/home.html', context)

def page_not_found(request, *args, **argv):
    return render(request, 'pybo/404.html', {})

def server_error(request, *args, **argv):
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
    student.card_set.create(to=request.GET.get('loc'), why='', moving_date=timezone.now(), ip=get_client_ip(request))
    return redirect('pybo:table')

def toQuick(request):
    num = request.POST.get('num')
    stu = Student.objects.filter(num=num).first()

    page = request.GET.get('page', '1')
    card = stu.card_set.order_by('-moving_date')

    paginator = Paginator(card, 10)
    page_obj = paginator.get_page(page)
    context = {'student': stu, 'card': page_obj}
    return render(request, 'pybo/quick.html', {'student': stu, 'card': page_obj})

def Quick(request, stu_num):
    stu = Student.objects.filter(num=stu_num).first()
    page = request.GET.get('page', '1')
    card = stu.card_set.order_by('-moving_date')

    paginator = Paginator(card, 10)
    page_obj = paginator.get_page(page)
    context = {'student': stu, 'card': page_obj}
    return render(request, 'pybo/quick.html', {'student': stu, 'card': page_obj})

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
                elif '재실' == to.to:
                    color = '#e0dede'
                    to = ''
                else:
                    if '화장실' == to.to:
                        color = '#ffb056'
                        to = to.to
                    elif '장탁이용중' == to.to:
                        color = '#569fff'
                        to = to.to
                    elif '특별실' == to.to[:3]:
                        color = '#af6ef3'
                        to = to.to[4:-1]
                    elif '조퇴' == to.to:
                        color = '#FF350A'
                        to = to.to
                    else:
                        color = '#43DC6C'
                        to = to.to


                bat[i].append([batch[i][j], s.name, color, to])
            else:
                bat[i].append([0])
    return render(request, 'pybo/TABLE.html', {'stu': Student.objects, 'batch': bat})

def toolbox(request):
    return render(request, 'pybo/toolbox.html')

def hmltolatex(request):
    return render(request, 'pybo/hmltolatex.html')

def neis(request):
    return render(request, 'pybo/neis.html')

def conv(request):
    if request.method == 'POST':
        hwp_equation = request.POST.get('equation', '')
        try:
            latex_equation = hp.hmlEquation2latex(hwp_equation)
            return JsonResponse({'latex': latex_equation})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def name(request):
    if request.method == 'GET' and 'loc' in request.GET:
        loc_values = request.GET.getlist('loc')  # 'loc'이라는 name을 가진 모든 값들을 리스트로 가져옴
        slib = [Student.objects.get(num=int(loc_values[i][:4])) for i in range(len(loc_values))]
        request.session['slib'] = [stu.id for stu in slib]  # Student ID 목록을 세션에 저장
        return redirect('pybo:PreCard_create_many')  # URL 패턴 이름으로 리디렉션
    else:
        stu_list = Student.objects.all()
        lib = [str(stu.num) + str(stu.name) for stu in stu_list]
        return render(request, 'pybo/name.html', {'lib': lib})


def PreCard_create_many(request):
    slib_ids = request.session.get('slib', [])
    slib = Student.objects.filter(id__in=slib_ids)  # 세션에서 Student ID 목록을 가져와 조회

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            for time_choice in list(eval(form.save(commit=False).time)):
                card = PreCard(
                    why=form.save(commit=False).why,
                    to="특별실(" + form.save(commit=False).to + ")",
                    moving_date=timezone.now(),
                    time=time_choice,
                    pw=form.save(commit=False).pw,
                    ip=get_client_ip(request)
                )
                card.save()  # 먼저 저장해야 ManyToMany 관계를 설정할 수 있음

                card.stus.set(slib)
                card.save()

            return redirect('pybo:home')
        else:
            # 폼 에러를 출력하여 디버깅
            print("폼 유효성 검사 실패")
            print(form.errors)
            print("POST 데이터:", request.POST)
    else:
        form = CardForm()

    return render(request, 'pybo/question_form_many.html', {'form': form, 'slib': slib})

def check_spelling(request):
    user_text = request.GET.get('text', '')

    if not user_text:
        return JsonResponse({'error': 'No text provided'}, status=400)

    url = "https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy"
    params = {
        'passportKey': 'bc39621223a128b948d3e8748a175a2263e575ac',
        'q': user_text,
        'where': 'nexearch',
        'color_blindness': 0,
        '_callback': 'spellCheckCallback',
        '_': int(time.time() * 1000)  # Unix 타임스탬프 밀리초
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        # 네이버의 JSONP 응답에서 JSON만 추출
        content = response.text
        json_str = content[content.find('(') + 1:-2]

        try:
            data = json.loads(json_str)
            result = data['message']['result']
            corrected_text = result['html']
            errors = ', '.join([f"{err['orgStr']} => {err['candWord']}" for err in result.get('errata_list', [])])

            return JsonResponse({
                'correctedText': corrected_text,
                'errors': errors,
                'errata_count': result['errata_count']
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': 'Failed to parse response', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Failed to contact spelling service'}, status=response.status_code)

def status_board(request):
    stus = Student.objects.prefetch_related('card_set').all()
    rest = []
    standing = []
    etc = []
    out = []

    def format_timedelta(td):
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f'{hours}시간 {minutes}분'

    for stu in stus:
        last_card = stu.card_set.last()
        if last_card:
            # last_card의 moving_date와 현재 시간을 비교
            last_card_date = last_card.moving_date.astimezone(timezone.get_current_timezone()).date()
            current_date = timezone.now().astimezone(timezone.get_current_timezone()).date()
    
            if last_card_date == current_date:
                time_diff = timezone.now() - last_card.moving_date
                formatted_time_diff = format_timedelta(time_diff)
                if '재실' not in last_card.to:
                    if '화장실' in last_card.to:
                        rest.append((last_card, formatted_time_diff))
                    elif '장탁' in last_card.to:
                        standing.append((last_card, formatted_time_diff))
                    elif '특별실' in last_card.to:
                        out.append((last_card, formatted_time_diff))
                    else:
                        etc.append((last_card, formatted_time_diff))
    
    return render(request, 'pybo/status_board.html', {
        'rest': rest,
        'standing': standing,
        'out': out,
        'etc': etc,
        'ctime': timezone.now()
    })


def reset(request):
    stu = Student.objects.all()
    for i in stu:
        card = Card(stu = i, to='재실', why='관리자에 의해 초기화되었습니다.', moving_date=timezone.now(),
                                ip=get_client_ip(request))
        card.save()

    return table(request)

def view_precard(request):
    page = request.GET.get('page', '1')  # 페이지
    current_view = request.GET.get('view', 'table')

    pcard = []
    time = []
    for i in PreCard.objects.all():
        if i.moving_date.date() == timezone.now().date():
            pcard.append([i, (i.moving_date + timedelta(hours=9)).time(), i.to[4:-1]])

    paginator = Paginator(pcard, 8)
    page_obj = paginator.get_page(page)
    context = {'pcard': page_obj, 'current_view': current_view}
    return render(request, 'pybo/view_precard.html', context)

def password(request, pcard_id, task):
    precard = get_object_or_404(PreCard, id=pcard_id)

    if request.method == 'POST':
        entered_pw = str(request.POST.get('password'))
        if entered_pw == str(precard.pw) or entered_pw == '221229':
            if task == 1:
                precard.delete()
                return redirect('pybo:view_precard')

        return render(request, 'pybo/password.html', {'error': '비밀번호가 일치하지 않습니다.', 'pcard_id': pcard_id, 'task': task})

    return render(request, 'pybo/password.html', {'pcard_id': pcard_id, 'task': task})