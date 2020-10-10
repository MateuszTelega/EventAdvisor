from django.contrib import admin
from .models import Event, EventType, Comment
from accounts.models import User

admin.site.register(Event)
admin.site.register(User)
admin.site.register(EventType)
admin.site.register(Comment)

