from core.views import EventListView


class IndexView(EventListView):
    template_name = 'index.html'
