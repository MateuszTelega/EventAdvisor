from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .models import Event
from .forms import EventForm


class EventListView(ListView):
    model = Event

    def get_queryset(self):
        return super().get_queryset().order_by('date_from', 'start_time')

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)
        permission = 0
        if not self.request.user.is_anonymous:
            permission = self.request.user.is_organizer
        context['permission'] = permission
        return context


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_organizer


class EventCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    title = 'Add Event'
    template_name = 'form.html'
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('index')

    def handle_no_permission(self):
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        permission = 0
        if not self.request.user.is_anonymous:
            permission = self.request.user.is_organizer
        context['permission'] = permission
        return context


class EventDetailView(DetailView):
    template_name = 'event_detail.html'
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        permission = 0
        if not self.request.user.is_anonymous:
            permission = self.request.user.is_organizer
        context['permission'] = permission
        return context


class SearchEventView(ListView):
    model = Event
    template_name = 'search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchEventView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Event.objects.filter(title__contains=query)
            result = postresult
        else:
            result = None
        return result

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)
        permission = 0
        if not self.request.user.is_anonymous:
            permission = self.request.user.is_organizer
        context['permission'] = permission
        return context
