from __future__ import unicode_literals
import os
from django.db import models


class UploadFile(models.Model):
    username = models.CharField(max_length=100, default='admin')
    filename = models.CharField(max_length=1000, default='admin_file')
    file = models.FileField(upload_to='files/%Y/%m/%d')

    def __str__(self):
        return self.filename

    def file_path(self):
        return self.file
        # return os.path.basename(self.file.name)


class Task(models.Model):
    filename = models.CharField(max_length=1000)
    username = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default="Finished")

    def __str__(self):
        return self.username + "--" + self.filename + "--" + self.status
