from django.shortcuts import render
from django.views.generic import View
from .models import ServiceActivity
from service_inform.models import ServiceObject


class IndexView(View):
    def get(self, request):
        context = dict()
        recent_activity = ServiceActivity.objects.recent_activity()
        recent_activity_date = ServiceActivity.objects.recent_activity_date()
        recent_service_objects_count = ServiceObject.objects.count_the_recent_number()
        sum_service_objects_count = ServiceObject.objects.count_the_sum_number()
        context['recent_activity_date'] = recent_activity_date
        context['recent_activity_place'] = recent_activity.place
        context['int_id'] = recent_activity.int_id
        context['recent_activity_flag'] = recent_activity.flag
        context['recent_service_objects_count'] = recent_service_objects_count
        context['sum_service_objects_count'] = sum_service_objects_count
        # we can show our team members in the front end if we like
        return render(request, 'service_activity/index.html', context=context)
