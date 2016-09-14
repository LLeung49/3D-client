from django import forms
from .models import HistoryTask


class HistoryTaskForm(forms.Form):
    user = forms.CharField(max_length=50)
    desc = forms.CharField(max_length=1000)
    file = forms.FileField()
