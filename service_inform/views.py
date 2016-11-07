from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View

# import string
# import random
import datetime

from service_activity.models import ServiceActivity
from .forms import ServiceObjectForm
from .models import ServiceObject
from .tools.generators import ShortLink, SerialNumber


class ServiceFormView(View):
    template_name = 'service_inform/service_form.html'
    redirect_view_name = 'service_inform:own_flag'

    def get(self, request):
        form = ServiceObjectForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        send_time = datetime.datetime.now()
        # we don't need to use the random code
        # random_code = ''.join([(string.ascii_letters + string.digits)[x] for x in random.sample(range(0, 62), 8)])
        flag = '修理中'
        form = ServiceObjectForm(request.POST)
        if form.is_valid():
            service_object = ServiceObject(**form.cleaned_data, send_time=send_time, flag=flag)
            service_object.service_activity = ServiceActivity.objects.recent_activity()
            service_object.save()
            service_object.short_link = ShortLink(service_object.pk).generate()
            service_object.serial_number = SerialNumber(service_object.pk, service_object.tel).generate()
            service_object.save()
            messages.add_message(request, messages.SUCCESS, '提交成功')

            print('生成短连接:' + service_object.short_link)
            print('生成取货号:' + service_object.serial_number)

            return HttpResponseRedirect(
                reverse(self.redirect_view_name, kwargs={'pk': service_object.pk, 'tel': service_object.tel}))
        else:
            messages.add_message(request, messages.WARNING, '表单有误')
            return render(request, self.template_name, {'form': form})


class ShortLinkRedirect(View):
    redirect_view_name = 'service_inform:own_flag'

    def get(self, request, short_link):
        s = get_object_or_404(ServiceObject, short_link=short_link)
        pk = s.pk
        tel = s.tel
        return HttpResponseRedirect(reverse(self.redirect_view_name, kwargs={'pk': pk, 'tel': tel}))


class OwnFlagView(View):
    template_name = 'service_inform/own_flag.html'

    def get(self, request, tel, pk):
        s = get_object_or_404(ServiceObject, pk=pk)
        # if the date of this service is not today, we regard it as illegal
        if datetime.date.today() != s.send_time.date():
            return HttpResponse('<h1>该服务对象已过期</h1>')
        context = dict()
        context['name'] = s.name
        context['computer_model'] = s.computer_model
        context['problem'] = s.problem
        context['flag'] = s.flag
        if s.flag == '遇到问题需反馈':
            context['trouble'] = s.trouble
        return render(request, self.template_name, context=context)
