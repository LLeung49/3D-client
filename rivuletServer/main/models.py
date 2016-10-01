from __future__ import unicode_literals
import os
from django.db import models


class UploadFile(models.Model):
    username = models.CharField(max_length=100, default='admin')
    filename = models.CharField(max_length=1000, default='admin_file')
    file = models.FileField(upload_to='raw_files/%Y/%m/%d')

    def __str__(self):
        return self.filename

    def file_path(self):
        return str(self.file)
        # return os.path.basename(self.file.name)


class Task(models.Model):
    filename = models.CharField(max_length=1000)
    username = models.CharField(max_length=100)
    outfile_name = models.CharField(max_length=1000, default="b")
    outfile_location = models.CharField(max_length=1000, default="a")
    task_id = models.CharField(max_length=1000, default="a")
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.username + "--" + self.filename + "--" + self.status



