from django.conf.urls import  include, url
from . import views
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^new_task/$', views.new_task, name='task')
    ]