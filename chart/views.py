# chart/views.py
from django.shortcuts import render
from django.db.models.functions import Cast
from .models import Passenger
import json
import pandas as pd
from django.db.models import Count, Q
from django.db.models import FloatField

def home(request):
    return render(request, 'home.html')

def covid_19(request):
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv', parse_dates=['Date'])
    countries = ['Japan', 'Colombia', 'Korea, South', 'Poland', 'Greece']

    df = df[df['Country'].isin(countries)]
    df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)
    df = df.pivot(index='Date', columns='Country', values='Cases')

    countries = list(df.columns)
    covid = df.reset_index('Date')
    covid.set_index(['Date'], inplace=True)
    covid.columns = countries
    populations = {'Colombia': 50882891, 'Greece': 10423054, 'Japan': 126476461, 'Korea, South': 51269185, 'Poland': 37846611}

    percapita = covid.copy()
    for country in list(percapita.columns):
        percapita[country] = percapita[country]/populations[country]*1000000

    return render(request, 'covid_19.html', {"Colombia": percapita["Colombia"].values, "Greece": percapita["Greece"].values,
                                      "Japan": percapita["Japan"].values, "Korea": percapita["Korea, South"].values,
                                      "Poland": percapita["Poland"].values})

def ticket_class_view_2(request):
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False)),
                  survival_rate=Cast(Count('ticket_class', filter=Q(survived=True)), FloatField())/Cast(Count('ticket_class'),FloatField())*100
    ) \
        .order_by('ticket_class')


    # 빈 리스트 3종 준비
    categories = list()             # for xAxis
    survived_series = list()        # for series named 'Survived'
    not_survived_series = list()    # for series named 'Not survived'
    rate_series = list()


    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])    # for xAxis
        survived_series.append(entry['survived_count'])          # for series named 'Survived'
        not_survived_series.append(entry['not_survived_count'])  # for series named 'Not survived'
        rate_series.append(entry['survival_rate'])


    # json.dumps() 함수로 리스트 3종을 JSON 데이터 형식으로 반환
    return render(request, 'ticket_class_2.html', {
        'categories': json.dumps(categories),
        'survived_series': json.dumps(survived_series),
        'not_survived_series': json.dumps(not_survived_series),
        'rate_series': json.dumps(rate_series)
    })