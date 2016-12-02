import urllib.parse

from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

# import string
# import random
import datetime
import json

from service_activity.models import ServiceActivity
from django.conf import settings
from .forms import ServiceObjectForm
from .models import ServiceObject, SMS_Feedback
from .tools.generators import ShortLink, SerialNumber
from .tools.calc_sign import sign_good


class ServiceFormView(View):
    template_name = 'service_inform/service_form.html'
    redirect_view_name = 'service_inform:own_flag'
    no_service_name = 'service_inform/no_service.html'

    def get(self, request):
        service_activity = ServiceActivity.objects.recent_activity()
        if service_activity is None or service_activity.flag == '已完成':
            # return HttpResponse('<h1>目前没有开放的维修活动</h1>')
            messages.add_message(request, messages.WARNING, '目前没有开放的维修活动')
            return render(request, self.no_service_name)
        else:
            if service_activity.flag == '预约中':
                messages.add_message(request,messages.INFO,'目前没有进行中的维修活动！<p>但是你可以预约 ' + service_activity.activity_date.strftime('%Y-%m-%d') + ' 全天</p><p>在 ' + service_activity.place +' 的维修服务</p>',extra_tags='safe')
            form = ServiceObjectForm()
            return render(request, self.template_name, {'form': form})

    def post(self, request):
        send_time = datetime.datetime.now()
        # we don't need to use the random code
        # random_code = ''.join([(string.ascii_letters + string.digits)[x] for x in random.sample(range(0, 62), 8)])
        flag = '待确认'
        form = ServiceObjectForm(request.POST)
        if form.is_valid():
            service_object = ServiceObject(**form.cleaned_data, send_time=send_time, flag=flag)
            service_object.service_activity = ServiceActivity.objects.recent_activity()
            if service_object.service_activity:
                service_object.save()
                service_object.short_link = ShortLink(service_object.pk).generate()
                service_object.serial_number = SerialNumber(service_object.pk).generate()
                service_object.save()
                messages.add_message(request, messages.INFO, '提交成功！<p>工作人员确认后会给你的手机发送取货码～</p>',extra_tags='safe')

                print('生成短连接:' + service_object.short_link)
                print('生成取货号:' + service_object.serial_number)

                return HttpResponseRedirect(
                    reverse(self.redirect_view_name, kwargs={'pk': service_object.pk, 'tel': service_object.tel}))
            else:
                # return HttpResponse('<h1>目前没有开放的维修活动</h1>')
                messages.add_message(request, messages.WARNING, '目前没有开放的维修活动')
                return render(request, self.no_service_name)
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
    no_service_name = 'service_inform/no_service.html'
    def get(self, request, tel, pk):
        service_activity = ServiceActivity.objects.recent_activity()
        s = get_object_or_404(ServiceObject, pk=pk)
        # if the date of this service is not today, we regard it as illegal
        if datetime.date.today() != s.send_time.date():
            messages.add_message(request, messages.WARNING, '本次活动已结束')
            # return HttpResponse('<h1>该服务对象已过期</h1>')
            return render(request, self.no_service_name)
        context = dict()
        context['place'] = service_activity.place
        context['name'] = s.name
        context['computer_model'] = s.computer_model
        context['problem'] = s.problem
        context['flag'] = s.flag
        if s.flag == '遇到问题需反馈':
            context['trouble'] = s.trouble
        return render(request, self.template_name, context=context)

@csrf_exempt
def sms_feedback(request):
    if request.method == 'POST':
        raw_sms_reply = request.POST.get('sms_reply')
        if raw_sms_reply:
            sms_reply_json = urllib.parse.unquote(raw_sms_reply)
            sms_reply = json.loads(sms_reply_json)
            '''
            if not sign_good(sms_reply, settings.APIKEY):  # validate the sign
                print('Fake feedback!')
                return HttpResponse("Invalid signature" )
            '''
            tel = sms_reply['mobile']
            reply_time = sms_reply['reply_time'].replace("+"," ")
            text = sms_reply['text']
            service_object = ServiceObject.objects.filter(tel=tel)[0]
            responsible_email = service_object.service_activity.responsible_email
            feedback = SMS_Feedback(text=text, reply_time=reply_time, service_object=service_object)
            feedback.save()  # put the data of feedback into our db
            # we are not going to trigger a signal,just send email in this view
            kwargs = {'subject': '来自' + tel + '的短信回复',
                      'message': 'Message received at ' + reply_time + '\n\nPickup number is ' +
			  service_object.serial_number + '\n\nName is ' + service_object.name + '\n\n' + text,
                      'from_email': 'HUSTCA <info@hustca.com>',
                      'recipient_list': [responsible_email, ]}
                     #'recipient_list': ['info@hustca.com' ]}
            if send_mail(**kwargs):
                print('成功发送邮件至' + responsible_email)
            else:
                print('邮件发送失败')
        else:
            print('于', str(datetime.datetime.now()), '收取回复失败')
        return HttpResponse("SUCCESS")
    else:
        return HttpResponse("Method not supported", status=405)

