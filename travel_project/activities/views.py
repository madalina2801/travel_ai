from django.views.generic import ListView, DetailView
from .models import Activity, CLIMATE_CHOICES, INTEREST_CHOICES

class ActivityListView(ListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    context_object_name = 'activities'
    paginate_by = 10  # Number of activities per page

    def get_queryset(self):
        queryset = super().get_queryset()

        climate= self.request.GET.get('climate')
        interest= self.request.GET.get('interest_type')
        if climate:
            queryset = queryset.filter(climate=climate)
        if interest:
            queryset = queryset.filter(interest_type=interest)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CLIMATE_CHOICES'] = CLIMATE_CHOICES
        context['INTEREST_CHOICES'] = INTEREST_CHOICES
        return context
    
class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activities/activity_detail.html'


# Create your views here.
