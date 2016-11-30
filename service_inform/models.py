from django.db import models
from service_activity.models import ServiceActivity


class ServiceObjectManager(models.Manager):
    def the_most_recent_service_objects(self):
        '''返回最近一次维修活动的所有服务对象'''
        # Be careful! The lib 'pytz' must be installed!
        most_recent_date = ServiceActivity.objects.recent_activity_date()
        service_objects = self.get_queryset().filter(send_time__date=most_recent_date)
        return service_objects

    def count_the_recent_number(self):
        '''返回最近一次维修活动的服务对象数目'''
        return len(self.the_most_recent_service_objects())

    def count_the_sum_number(self):
        '''返回所有对象数目'''
        return len(self.get_queryset())


class ServiceObject(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=16)
    tel = models.CharField(verbose_name='电话', max_length=11)
    computer_model = models.CharField(verbose_name='电脑品牌/型号', blank=True, max_length=64)
    problem = models.TextField(verbose_name='电脑故障')

    send_time = models.DateTimeField(verbose_name='送到时间', auto_now_add=True)
    FLAGS = (('完成', '完成'), ('修理中', '修理中'), ('已取回', '已取回'), ('遇到问题需反馈', '遇到问题需反馈'))
    flag = models.CharField(verbose_name='修理状态', max_length=64, choices=FLAGS)
    trouble = models.TextField(verbose_name='遇到的问题', blank=True)
    short_link = models.CharField(verbose_name='短链接', max_length=32)
    serial_number = models.CharField(verbose_name='取货号', max_length=16)

    service_activity = models.ForeignKey(ServiceActivity, related_name='service_objects', verbose_name='从属哪次活动')

    objects = ServiceObjectManager()

    def __str__(self):
        return self.name + '-' + self.short_link

    class Meta:
        verbose_name = '服务对象'
        verbose_name_plural = '服务对象'


class SMS_Feedback(models.Model):
    text = models.CharField(verbose_name='短信回复内容', max_length=256)
    reply_time = models.DateTimeField(verbose_name='回复短信时间')

    service_object = models.ForeignKey(ServiceObject, related_name='sms_feedback', verbose_name='从属哪个服务对象')

    def __str__(self):
        return self.service_object + '的短信回复'

    class Meta:
        verbose_name = '短信回复'
        verbose_name_plural = '短信回复'
