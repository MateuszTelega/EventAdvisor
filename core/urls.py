from django.urls import path

from .views import EventCreateView

app_name = 'core'
urlpatterns = [
    path('event/create', EventCreateView.as_view(), name='event_create'),
]
