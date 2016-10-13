from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    rank = models.CharField(max_length=10, default='Normal')
    capacity = models.IntegerField(default=500)
    storage_used = models.FloatField(default=0)

    def __str__(self):
        return self.user.username + '--' + self.rank
