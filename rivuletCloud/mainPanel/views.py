from django.shortcuts import render, render_to_response, get_object_or_404
from .models import HistoryTask
from django.views.generic.edit import CreateView
from django.views import generic
from django import forms
from django.http import HttpResponse


class UserForm(forms.Form):
    username = forms.CharField()
    time = forms.DateTimeField()
    filename = forms.CharField()
    file_field = forms.FileField()


def homepage(request):
    return render_to_response('mainPanel/homepage.html')

    # return HttpResponse(template.render(context, request))
    # return render(request, 'mainPanel/homepage.html')


class HistoryCreate(CreateView):
    model = HistoryTask
    fields = ['user','task_desc', 'file_field']


class HistoryView(generic.ListView):
    template_name = 'mainPanel/history.html'
    context_object_name = "history_list"

    def get_queryset(self):
        return HistoryTask.objects.all()
