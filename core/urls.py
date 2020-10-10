from django.urls import path

from .views import EventCreateView, EventDetailView, SearchEventView


app_name = 'core'
urlpatterns = [
    path('event/create', EventCreateView.as_view(), name='event_create'),
    path('event/detail/<pk>', EventDetailView.as_view(), name='event_detail'),
    path('event/search', SearchEventView.as_view(), name='event_search'),
]
