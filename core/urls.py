from django.urls import path

from .views import EventCreateView, EventUpdateView, EventDetailView, SearchEventView


app_name = 'core'
urlpatterns = [
    path('event/create', EventCreateView.as_view(), name='event_create'),
    path('event/update/<pk>', EventUpdateView.as_view(), name='event_update'),
    path('event/detail/<pk>', EventDetailView.as_view(), name='event_detail'),
    path('event/search', SearchEventView.as_view(), name='event_search'),
]
