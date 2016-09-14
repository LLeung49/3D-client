from django.db import models
from django.core.urlresolvers import reverse


class HistoryTask(models.Model):
    user = models.CharField(max_length=1000, default='Admin')
    task_desc = models.CharField(max_length=1000, default='Please input descriptions')
    file_field = models.FileField()

    def get_absolute_url(self):
        return reverse('mainPanel:history')

    def __str__(self):
        return self.user + ' -  ' + self.task_desc

