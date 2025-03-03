from django.http import JsonResponse
# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from .models import *
from .forms import *
from .crolling import meal, update_meal
from .subject import subject
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
    sub = subject(int(day))

    context = {
        'b': list(map(str, dish['breakfast'].split(','))),
        'l': list(map(str, dish['lunch'].split(','))),
        'd': list(map(str, dish['dinner'].split(','))),
        't': dish['date'],
        'day': day,
        'sub': [
            (sub['1'], '1'),
            (sub['2'], '2'),
            (sub['3'], '3'),
            (sub['4'], '4'),
            (sub['A'], 'A'),
            (sub['B'], 'B'),
        ]
    }

    if datetime.now().hour >= 14:
        context['ex'] = '3'
    elif datetime.now().hour >= 8:
        context['ex'] = '2'
    else:
        context['ex'] = '1'

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
    to = Card.objects.filter(stu=stu).order_by('-moving_date').first()
    if to.to != '재실':
        stu.card_set.create(to='재실', why='', moving_date=timezone.now(), ip=get_client_ip(request))
        return redirect('pybo:table')
    else:
        page = request.GET.get('page', '1')
        card = stu.card_set.order_by('-moving_date')

        paginator = Paginator(card, 10)
        page_obj = paginator.get_page(page)
        context = {'student': stu, 'card': page_obj}
        return render(request, 'pybo/quick.html', {'student': stu, 'card': page_obj})

def table(request):
    batch = [[0000, 0000, 0000, 0000, 2111, 2110, 0000, 0000, 0000, 2106, 2105, 0000, 2103, 0000, 0000],
             [0000, 0000, 2116, 0000, 2118, 2119, 0000, 0000, 2202, 2203, 2204, 0000, 2206, 0000, 2208],
             [0000, 0000, 0000, 2220, 2219, 2218, 0000, 2216, 2215, 0000, 0000, 2212, 2211, 2210, 2209],
             [0000, 0000, 0000, 2302, 2303, 0000, 0000, 0000, 0000, 0000, 0000, 2310, 0000, 0000, 2313],
             [0000, 0000, 0000, 0000, 2404, 2403, 2402, 2401, 0000, 2319, 0000, 0000, 2316, 2315, 2314],
             [0000, 0000, 2408, 0000, 0000, 0000, 2412, 2413, 0000, 2415, 0000, 0000, 0000, 0000, 2420]]

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
                    elif '퇴사' == to.to:
                        color = '#5154ea'
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
        slib = []
        for val in loc_values:
            if val:
                tmp = str(val)
                if tmp[:4].isdigit() == True:
                    slib.append(Student.objects.get(num=int(tmp[:4])))
                elif tmp[:3].isalpha() == True:
                    slib.append(Student.objects.get(name=str(tmp[:3])))

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

            return redirect('pybo:view_precard')
        else:
            # 폼 에러를 출력하여 디버깅
            print("폼 유효성 검사 실패")
            print(form.errors)
            print("POST 데이터:", request.POST)

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
            elif task == 2:
                request.session['pcard_id'] = pcard_id
                return redirect('pybo:name_re')
        return render(request, 'pybo/password.html', {'error': '비밀번호가 일치하지 않습니다.', 'pcard_id': pcard_id, 'task': task})

    return render(request, 'pybo/password.html', {'pcard_id': pcard_id, 'task': task})


def name_re(request):
    if request.method == 'GET' and 'loc' in request.GET:
        loc_values = request.GET.getlist('loc')  # 'loc'이라는 name을 가진 모든 값들을 리스트로 가져옴
        slib = []
        for val in loc_values:
            if val:
                slib.append(Student.objects.get(num=int(val[:4])))

        request.session['slib'] = [stu.id for stu in slib]  # Student ID 목록을 세션에 저장
        return redirect('pybo:PreCard_create_many_re')  # URL 패턴 이름으로 리디렉션
    else:
        stu_list = Student.objects.all()
        lib = [str(stu.num) + str(stu.name) for stu in stu_list]

        pcard_id = request.session['pcard_id']
        stu_list = list(PreCard.objects.filter(id=pcard_id).last().stus.all())
        stu_list.append('')
        return render(request, 'pybo/name_re.html', {'lib': lib, 'stu_list': stu_list})


def PreCard_create_many_re(request):
    slib_ids = request.session.get('slib', [])
    slib = Student.objects.filter(id__in=slib_ids)  # 세션에서 Student ID 목록을 가져와 조회
    Pcard = get_object_or_404(PreCard, id=request.session['pcard_id'])

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            Pcard.delete()
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

            return redirect('pybo:view_precard')
        else:
            # 폼 에러를 출력하여 디버깅
            print("폼 유효성 검사 실패")
            print(form.errors)
            print("POST 데이터:", request.POST)

    Pcard.to = Pcard.to[4:-1]
    Pcard.save()
    form = CardForm(instance=Pcard)
    Pcard.to = f"특별실({Pcard.to})"
    Pcard.save()
    return render(request, 'pybo/question_form_many_re.html', {'form': form, 'slib': slib})

def set_meal(request, s, e):
    update_meal(s, e)

    import os
    from django.http import HttpResponse
    file_path = os.path.join('meal_info.txt')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except FileNotFoundError:
        return HttpResponse("File not found.", content_type="text/plain")

    return HttpResponse(file_content, content_type="text/plain;charset=utf-8")


def add_students(request):
    students_data = [
        ("3414", "황재훈"), ("3413", "함세빈"), ("3412", "최이량"), ("3411", "조우성"),
        ("3410", "전정민"), ("3409", "이혜안"), ("3408", "신우진"), ("3407", "신동현"),
        ("3406", "송정현"), ("3405", "노영서"), ("3404", "김정택"), ("3403", "김도건"),
        ("3402", "권가현"), ("3401", "강정연"), ("3314", "황세하"), ("3313", "허율"),
        ("3312", "정효림"), ("3311", "이준혁"), ("3310", "이우혁"), ("3309", "이영헌"),
        ("3308", "윤태현"), ("3307", "오건"), ("3306", "서민준"), ("3305", "박형기"),
        ("3304", "도성민"), ("3303", "김윤완"), ("3302", "김성윤"), ("3301", "김도연"),
        ("3214", "홍수현"), ("3213", "조정안"), ("3212", "임준희"), ("3211", "이동빈"),
        ("3210", "윤수인"), ("3209", "우은서"), ("3208", "신정훈"), ("3207", "박채은"),
        ("3206", "도수현"), ("3205", "김정운"), ("3204", "김승민"), ("3203", "김민준"),
        ("3202", "김리원"), ("3201", "김대훈"), ("3113", "황예준"), ("3112", "황소언"),
        ("3111", "정지후"), ("3110", "정재윤"), ("3109", "장지호"), ("3108", "임지원"),
        ("3107", "백경훈"), ("3106", "배윤희"), ("3105", "김한음"), ("3104", "김소현"),
        ("3103", "김도유"), ("3102", "권호승"), ("3101", "강나연")
    ]

    students = [Student(num=num, name=name) for num, name in students_data]
    Student.objects.bulk_create(students)  # ✅ 한 번에 삽입
