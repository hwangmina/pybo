from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Program, Category, Recommendation
import pandas as pd
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q

import time


# Create your views here.
def downloadProgram(request):
    filename = 'C:/dataton2022/8월전체프로그램.csv'
    df = pd.read_csv(filename, encoding="UTF-8", na_values='nan')
    count = 0
    for i in range(len(df)):
        # 기간 format 변경 (str > date)
        start_date_string = df["행사기간시작일"][i]
        start_date_format = "%Y.%m.%d"
        start_date_result = datetime.strptime(start_date_string, start_date_format)
        end_date_string = df["행사기간종료일"][i]
        end_date_format = "%Y.%m.%d"
        end_date_result = datetime.strptime(end_date_string, end_date_format)
        # 프로그램 데이터 db에 저장
        Program.objects.create(name=df["프로그램명"][i], type=df["유형"][i],
                               category=df["카테고리"][i], host=df["행사시설명"][i], age=df["대상"][i],
                               price=df["수강료"][i], start_date=start_date_result, end_date=end_date_result,
                               link=df["안내URL"][i], coorx=df["X좌표값"][i], coory=df["Y좌표값"][i])
    return HttpResponse(f'''
    <html>
    <body>
        <h1>카테고리 이름</h1>
        <h1>Download Complete</h1>
        {len(df)}
        {count}
        <h2>Data Types</h2>
        {df.dtypes}
    </body>
    </html>
    ''')


def index(request):
    page = request.GET.get('page', '1')  # 페이지
    program_list = Program.objects.order_by('start_date')
    paginator = Paginator(program_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'program_list': page_obj}
    return render(request, 'program/program_list.html', context) # 객체 있으면 세번째 parameter: context


def detail(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    context = {'program': program}
    return render(request, 'program/program_detail.html', context)


def answer_create(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    context = {'program': program}
    return render(request, 'program/program_result.html', context)


def program_search(request):

    context = {}

    #사이트에서 필터 선택 여부 받아오기
    b = request.GET.get('b', '')
    f = request.GET.get('f', '')
    price = request.GET.get('price', '')
    program_list = Program.objects.order_by('-start_date')

    ########## 카테고리 리스트 ###############
    category_list = Category.objects.all()
    context['category_list'] = category_list

    if b:
        program_list = program_list.filter(
            Q(name__icontains=b) |
            Q(category__icontains=b)
        ).distinct()

    if f:
        program_list = program_list.filter(Q(category__icontains=f))

    if price == '0':
        program_list = program_list
    elif price == '1':
        program_list = program_list.filter(price=0)
    elif price == '2':
        program_list = program_list.filter(price__lte=20000)
    elif price == '3':
        program_list = program_list.filter(Q(price__gt=20000)&Q(price__lte=30000))
    elif price == '4':
        program_list = program_list.filter(Q(price__gt=30000)&Q(price__lte=40000))
    elif price == '5':
        program_list = program_list.filter(Q(price__gt=40000)&Q(price__lte=50000))
    elif price == '6':
        program_list = program_list.filter(price__gt=50000)
    else:
        program_list = program_list

    # 필터 옵션
    context['b'] = b
    context['f'] = f
    context['price'] = price

    # 필터링 된 결과 개수
    context['program_number'] = program_list.count()

    # 페이징 처리 시작
    page = request.GET.get('page', '1')  # 페이지
    paginator = Paginator(program_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context['program_list'] = page_obj

    return render(request, 'program/program_search.html', context)



def downloadRecommendation(request):
    filename = 'C:/dataton2022/8월추천프로그램.csv'
    df = pd.read_csv(filename, encoding="UTF-8", na_values='nan')
    for i in range(len(df)):
        recommendlist = df["추천 프로그램"][i].split(', ')
        # 추천 데이터 db에 저장
        Recommendation.objects.create(name=df["프로그램명"][i],
                                      recommendation1=recommendlist[0], recommendation2=recommendlist[1][1:-1],
                                      recommendation3=recommendlist[2][1:-1], recommendation4=recommendlist[3][1:-1])
    return HttpResponse(f'''
    <html>
    <body>
    {df}
    </body>
    </html>
    ''')

