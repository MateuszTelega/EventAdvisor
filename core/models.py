from django.db import models
from accounts.models import User


class Event(models.Model):
    pass


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} comment {self.event} at {self.created}"
