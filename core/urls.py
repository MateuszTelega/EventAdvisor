from django.urls import path

from .views import EventCreateView, EventDetailView

app_name = 'core'
urlpatterns = [
    path('event/create', EventCreateView.as_view(), name='event_create'),
    path('event/detail/<pk>', EventDetailView.as_view(), name='event_detail'),
]
