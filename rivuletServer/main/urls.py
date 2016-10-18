from django.conf.urls import  include, url
from . import views
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^new_task/$', views.new_task, name='task'),
    url(r'^new_task/update_file/$', views.update_file, name='update_file'),
    url(r'^new_task/get_thumbnail/$', views.get_thumbnail, name='get_thumbnail'),
    # url(r'^new_order$', views.order, name='order'),
    ]