from django.views.generic import ListView

from .models import Event


class EventListView(ListView):
    model = Event

    def get_queryset(self):
        return super().get_queryset().order_by('date_from', 'start_time')
