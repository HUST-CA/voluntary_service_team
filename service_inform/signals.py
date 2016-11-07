from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ServiceObject
from .tools.SMS_Thread import SMSThread


@receiver(post_save, sender=ServiceObject)
def inform(sender, instance, created, **kwargs):
    if created:
        # this is the first time that the views.py invoke the save() method
        # the short_link has not been generated yet,so that we should abort this trigger
        return
    else:
        # this is what will happen after the post and the flag's default is '修理中'
        # accordingly, we send the receive sms
        if instance.flag == '修理中':
            SMSThread(receiver_mobile=instance.tel,
                      status='收到',
                      short_link=instance.short_link).start()
        # send the finish sms
        if instance.flag == '完成':
            SMSThread(receiver_mobile=instance.tel,
                      status='完成',
                      short_link=instance.short_link).start()
        # send the trouble sms
        elif instance.flag == '遇到问题需反馈':
            SMSThread(receiver_mobile=instance.tel,
                      status='遇到问题需反馈',
                      reason=instance.trouble).start()
        # when it comes to exceptions, just pass it
        else:
            pass
