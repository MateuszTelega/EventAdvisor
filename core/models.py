from django.db import models
from accounts.models import User


class EventType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    date_from = models.DateField()
    date_to = models.DateField()
    place = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    picture = models.ImageField(upload_to="media", null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    event_type = models.ForeignKey(EventType, null=True, blank=True, on_delete=models.SET_NULL)
    users = models.ManyToManyField(User, related_name='user')
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Event {self.title} starts {self.date_from} in {self.place}. Created {self.created}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} comment {self.event} at {self.created}"

