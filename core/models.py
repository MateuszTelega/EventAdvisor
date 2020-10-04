from django.db import models


class User(models.Model):
    pass


class Event(models.Model):
    title = models.CharField(max_length=100)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    place = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    users = models.ManyToManyField(User)

    def __str__(self):
        pass