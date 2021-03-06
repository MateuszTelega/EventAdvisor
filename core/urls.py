from django.urls import path
from .views import EventCreateView, EventUpdateView, EventDetailView, EventDeleteView, \
    SearchEventView, EventMyView, EventFilterView, post_comment
from .filters import EventFilter


app_name = 'core'
urlpatterns = [
    path('event/create', EventCreateView.as_view(), name='event_create'),
    path('event/update/<pk>', EventUpdateView.as_view(), name='event_update'),
    path('event/detail/<pk>', EventDetailView.as_view(), name='event_detail'),
    path('event/delete/<pk>', EventDeleteView.as_view(), name='event_delete'),
    path('event/search', SearchEventView.as_view(), name='event_search'),
    path('event/comment/<event_id>', post_comment, name='event_comments'),
    path('event/my', EventMyView.as_view(), name='event_user_section'),
    path('event/filter', EventFilterView.as_view(filterset_class=EventFilter, template_name='filter.html'),
         name='event_filter'),
]
