from django_filters import FilterSet, ChoiceFilter
from .models import Event


class EventFilter(FilterSet):

    CHOICES = (
        ('ascending', 'Newest Events'),
        ('descending', 'Oldest Events'),
    )

    #ordering = ChoiceFilter(label='Created', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Event
        fields = {
            'place': ['icontains'],
            'date_from': ['gt', 'lt'],
            'owner': ['exact'],
            'users': ['exact'],
        }

    def filter_by_order(self, queryset, name, value):
        expression = 'created' if value == 'ascending' else '-created'
        return queryset.order_by(expression)
