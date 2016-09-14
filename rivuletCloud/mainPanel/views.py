from django.shortcuts import render, render_to_response, get_object_or_404
from .models import HistoryTask
from django.views.generic.edit import CreateView
from django.views import generic
from django.core.urlresolvers import reverse
from django import forms
from .task_forms import HistoryTaskForm
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from .models import HistoryTask


def homepage(request):
    if request.method == 'POST':
        form = HistoryTaskForm(request.POST, request.FILES)
        if form.is_valid():
            new_task = HistoryTask(user=form.cleaned_data["user"], task_desc=form.cleaned_data["desc"], file_field=form.cleaned_data["file"])
            new_task.save()

            return HttpResponseRedirect(reverse('mainPanel:history'))
    else:
        form = HistoryTaskForm()

    data = {'form': form}
    return render_to_response('mainPanel/homepage.html')

    # return render_to_response('mainPanel/homepage.html')

    # return HttpResponse(template.render(context, request))


class HistoryCreate(CreateView):
    model = HistoryTask
    fields = ['user', 'task_desc', 'file_field']


class HistoryView(generic.ListView):
    template_name = 'mainPanel/history.html'
    context_object_name = "history_list"

    def get_queryset(self):
        return HistoryTask.objects.all()
