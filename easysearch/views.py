import datetime

from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from .config import *

es = Elasticsearch(ES_SERVER)


def get_epoch_seconds_from_date(dt):
    dt = str(dt)
    return (datetime.datetime.strptime(dt, "%Y-%m-%d").date() - datetime.date(1970, 1, 1)).total_seconds()


def EasySearch(request):
    return render(request, 'easysearch/home.html', {})

def SearchResults(request):
    result_list = process(
        request.POST.get('department', ''),
        request.POST.get('segment', ''),
        request.POST.get('category', ''),
        request.POST.get('fromdate', ''),
        request.POST.get('todate', ''),
        request.POST.get('query', ''),
    )
    paginator = Paginator(result_list, NUM_PAGINATOR_RESULTS)
    try:
        results = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    return render(request, 'easysearch/results.html', {
        'results': results,
        'num_pages': range(1, paginator.num_pages + 1),
    })


def process(department, segment, category, date_from, date_to, search_query):
    if len(date_from) == 0:
        date_from = 0.0
    else:
        date_from = get_epoch_seconds_from_date(date_from)

    if len(date_to) == 0:
        date_to = 999999999999999999.0
    else:
        date_to = get_epoch_seconds_from_date(date_to)

    squery = Search(using=es, index="files").query(
        "multi_match", query=search_query, fields=['title', 'information'])
    print("department", department, len(department))
    if len(department) != 0:
        squery = squery.filter("terms", department=department)
    if len(segment) != 0:
        squery = squery.filter("terms", segment=segment)
    if len(category) != 0:
        squery = squery.filter("terms", category=category)
    print("From: ", date_from)
    print("To: ", date_to)
    squery = squery.filter("range", lastmodified={
                           "lte": date_to, "gte": date_from})
    response = squery.execute()
    print("debug: ", response)
    return response