from core.views import EventListView


class IndexView(EventListView):
    template_name = 'index.html'


class AboutUs(EventListView):
    template_name = 'about_us.html'