from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

app_name = 'mainPanel'


urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^history/$', views.HistoryView.as_view(), name='history'),
    url(r'^upload/$', views.HistoryCreate.as_view(), name='task-upload'),
    # url(r'^upload_status/$', views.SaveTask, name='saved')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)