from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ServiceObject

@receiver(post_save,sender=ServiceObject)
def inform(sender, instance, created, **kwargs):
    # 说明此时是刚post完表单,发送通知短信
    if created:
        pass
    # 说明此时是修改了字段
    else:
        # 说明已完成,发送完成短信
        if instance.flag == '完成':
            pass
        # 说明遇到问题,发短信通知问题
        elif instance.flag == '遇到问题需反馈':
            pass
        # 其他情况直接pass就好,不需要发短信
        else:
            pass


