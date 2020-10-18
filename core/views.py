from datetime import date

import requests
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Event, Comment
from .forms import EventForm, CommentForm
from .filters import EventFilter
from django_filters.views import FilterView


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_organizer


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user_id = self.request.user.pk
        event = Event.objects.get(pk=self.request.path_info.split('/')[-1])
        event_owner_id = event.owner_id
        return event_owner_id == user_id


class EventListView(ListView):
    model = Event
    paginate_by = 3

    def get_queryset(self):
        return super().get_queryset().filter(date_to__gte=date.today()).order_by('date_from', 'start_time')

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)

        context['my_events'] = False

        permission = 0
        if not self.request.user.is_anonymous:
            permission = self.request.user.is_organizer
        context['permission'] = permission

        is_logged_in = False
        if self.request.user.is_authenticated:
            is_logged_in = True
        context['logged_in'] = is_logged_in

        context['filter'] = EventFilter(self.request.GET, queryset=self.get_queryset())

        return context


class EventMyView(LoginRequiredMixin, ListView):
    model = Event
    paginate_by = 3
    template_name = 'index.html'

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(users=user).order_by('date_from', 'start_time')

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)

        context['my_events'] = True

        permission = 0
        if not self.request.user.is_anonymous:
            permission = self.request.user.is_organizer
        context['permission'] = permission

        is_logged_in = False
        if self.request.user.is_authenticated:
            is_logged_in = True
        context['logged_in'] = is_logged_in

        context['filter'] = EventFilter(self.request.GET, queryset=self.get_queryset())

        return context


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

        is_logged_in = False
        if self.request.user.is_authenticated:
            is_logged_in = True
        context['logged_in'] = is_logged_in

        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EventUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        permission = 0
        if not self.request.user.is_anonymous:
            permission = self.request.user.is_organizer
        context['permission'] = permission

        is_logged_in = False
        if self.request.user.is_authenticated:
            is_logged_in = True
        context['logged_in'] = is_logged_in

        return context


class EventDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    template_name = 'event_confirm_delete.html'
    model = Event
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        permission = 0
        if not self.request.user.is_anonymous:
            permission = self.request.user.is_organizer
        context['permission'] = permission

        is_logged_in = False
        if self.request.user.is_authenticated:
            is_logged_in = True
        context['logged_in'] = is_logged_in

        return context


class EventDetailView(DetailView):
    template_name = 'event_detail.html'
    model = Event
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = {'comments': list(Comment.objects.filter(event=context['event'].id))}
        context.update(q)
        context.update({'add_comment': CommentForm()})

        permission = 0
        if not self.request.user.is_anonymous:
            permission = self.request.user.is_organizer
        context['permission'] = permission

        is_owner = False
        if self.request.user.pk == context['event'].owner_id:
            is_owner = True
        context['owner'] = is_owner

        is_logged_in = False
        if self.request.user.is_authenticated:
            is_logged_in = True
        context['logged_in'] = is_logged_in

        user = self.request.user
        event = self.model.objects.get(pk=context['event'].id)

        is_subscribed = False
        if is_logged_in and user in event.users.all():
            is_subscribed = True
        context['subscribed'] = is_subscribed
        context['users_list'] = ', '.join([user.name for user in event.users.all()])

        return context

    def post(self, request, pk):
        event = self.model.objects.get(pk=pk)
        user_subscribing = self.request.user

        if user_subscribing not in event.users.all():
            event.users.add(user_subscribing)
        else:
            event.users.remove(user_subscribing)
        event.save()

        return HttpResponseRedirect(reverse('core:event_detail', args=(pk,)))


class SearchEventView(ListView):
    model = Event
    template_name = 'search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchEventView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            lookups = Q(title__contains=query) | Q(owner__name__icontains=query) | Q(description__icontains=query)\
                      | Q(place__icontains=query) | Q(event_type__name__icontains=query)
            postresult = Event.objects.filter(lookups)
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

        is_logged_in = False
        if self.request.user.is_authenticated:
            is_logged_in = True
        context['logged_in'] = is_logged_in

        return context


class EventFilterView(FilterView):
    model = Event

    def get_queryset(self):
        super().get_queryset()

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)

        permission = 0
        if not self.request.user.is_anonymous:
            permission = self.request.user.is_organizer
        context['permission'] = permission

        is_logged_in = False
        if self.request.user.is_authenticated:
            is_logged_in = True
        context['logged_in'] = is_logged_in

        context['filter'] = EventFilter(self.request.GET, queryset=self.get_queryset())

        return context


def post_comment(request, *args, **kwargs):
    try:
        r = requests.post('http://agnesgru.pythonanywhere.com',
                          data={'wpisz_opinie': request.POST.get('comment')}).json()
        opinion = r['result_int']
    except Exception:
        opinion = None

    comment = Comment(comment=request.POST.get('comment'),
                      user_id=request.user.id,
                      event_id=kwargs['event_id'],
                      opinion=opinion,
                      )

    if request.user.id:
        comment.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, "You need to be login")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


