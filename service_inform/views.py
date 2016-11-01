from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

# import string
# import random
import datetime

from service_activity.models import ServiceActivity
from .forms import ServiceObjectForm
from .models import ServiceObject
from .tools.short_link_generator import ShortLink


class ServiceFormView(View):
    template_name = 'service_inform/service_form.html'
    redirect_view_name = 'service_inform:own_flag'

    def get(self, request):
        form = ServiceObjectForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        send_time = datetime.datetime.now()
        # random_code = ''.join([(string.ascii_letters + string.digits)[x] for x in random.sample(range(0, 62), 8)])
        flag = '修理中'
        form = ServiceObjectForm(request.POST)
        if form.is_valid():
            service_object = ServiceObject(**form.clean_data, send_time=send_time, flag=flag)
            service_object.service_activity = ServiceActivity.objects.recent_activity()
            service_object.save()
            service_object.short_link = ShortLink(service_object.pk).generate()
            service_object.save()
            messages.add_message(request, messages.SUCCESS, '提交成功')
            return HttpResponseRedirect(
                reverse(self.redirect_view_name, kwargs={'short_link': service_object.short_link}))
        else:
            messages.add_message(request, messages.WARNING, '表单有误')
            return render(request, self.template_name, {'form': form})


class OwnFlagView(View):
    template_name = 'service_inform/own_flag.html'

    def get(self, request, pk):
        s = get_object_or_404(ServiceObject, pk=pk)
        context = dict()
        context['name'] = s.name
        context['computer_model'] = s.computer_model
        context['problem'] = s.problem
        context['flag'] = s.flag
        if s.flag == '遇到问题需反馈':
            context['trouble'] = s.trouble
        return render(request, self.template_name, context=context)


class ShortLinkRedirect(View):
    view_name = 'service_inform:own_flag'

    def get(self, short_link):
        s = get_object_or_404(ServiceObject, short_link=short_link)
        pk = s.pk
        return HttpResponseRedirect(reverse(self.view_name, kwargs={'pk': pk}))
