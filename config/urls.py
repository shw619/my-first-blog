from django.contrib import admin
from django.urls import path, include
from chart import views                                     # !!!

urlpatterns = [
    path('',include('chart.urls')),
    path('covid_19/',
         views.covid_19, name='covid_19'),  # !!!
    path('admin/', admin.site.urls),
]