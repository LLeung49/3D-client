"""rivuletServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apscheduler.scheduler import Scheduler
from main.models import Task

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', include('login.urls', namespace='login', app_name='login'),),
    url(r'^main/', include('main.urls', namespace='main', app_name='main'),),
]



# sched = Scheduler()
#
#
# @sched.interval_schedule(seconds=1)
# def mytask():
#     all_files = Task.objects.filter(status="Queuing")
#     if all_files:
#         print("Fils in the queue")
#     else:
#         print("Queuing is empty")
#
# sched.start()
