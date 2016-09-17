from django.conf.urls import  include, url
from . import views
urlpatterns = [
    # url(r'^$', views.login, name='login'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    # url(r'^login/$', views.login, name='login'),
    ]