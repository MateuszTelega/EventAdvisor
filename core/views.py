from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import Event
from .forms import EventForm


class EventListView(ListView):
    model = Event

    def get_queryset(self):
        return super().get_queryset().order_by('date_from', 'start_time')


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_organizer


class EventCreateView(LoginRequiredMixin, OrganizerRequiredMixin, PermissionRequiredMixin, CreateView):
    title = 'Add Event'
    template_name = 'form.html'
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('index')
    permission_required = 'core.change_event'

    def handle_no_permission(self):
        return redirect('index')
