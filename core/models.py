from django.db import models
from accounts.models import User


class Event(models.Model):
    pass


class Comment(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField(max_length=200, null=False, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} comment {self.event} at {self.date}"
