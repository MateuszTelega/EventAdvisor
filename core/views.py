from django.views.generic import ListView

from .models import Event


class EventListView(ListView):
    model = Event
