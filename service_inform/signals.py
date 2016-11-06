from django.db.models.signals import post_save
from django.dispatch import receiver
from voluntary_service_team.secure_settings import APPKEY
from voluntary_service_team.secure_settings import SMS_TEMPLATE_CODE_INFORM
from voluntary_service_team.secure_settings import SMS_TEMPLATE_CODE_PROBLEM
from voluntary_service_team.secure_settings import SMS_TEMPLATE_CODE_SUCCESS
from .models import ServiceObject
from .send_SMS import tpl_send_sms
@receiver(post_save,sender=ServiceObject)
def inform(sender, instance, created, **kwargs):
    # 说明此时是刚post完表单,发送通知短信
    if created:
        """
        模板内容：【华科计算机协会】亲~你的电脑我们已经收到啦！提取码：#code1#，戳 https://huca.tech/#code# 可以查看维修进度哦~
        """
        code = 0
        param = {"#code#":code,"#code1#":code}
        phonenumber = 66666666
        tpl_send_sms(apikey=APPKEY,tpl_id=SMS_TEMPLATE_CODE_INFORM,tpl_value=param,mobile=phonenumber)
        pass
    # 说明此时是修改了字段
    else:
        # 说明已完成,发送完成短信
        if instance.flag == '完成':
            """
            	【华科计算机协会】亲亲亲！普天同庆！你的电脑已经维修完成啦！
                请凭 #code# 提取电脑哦！
                https://huca.tech/#code1#
            """
            code = 0
            param = {"#code#": code, "#code1#": code}
            phonenumber = 66666666
            tpl_send_sms(apikey=APPKEY, tpl_id=SMS_TEMPLATE_CODE_SUCCESS, tpl_value=param, mobile=phonenumber)
            pass
        # 说明遇到问题,发短信通知问题
        elif instance.flag == '遇到问题需反馈':
            """
            【华科计算机协会】亲~维修出现了问题嚎。原因：#reason#
            本短信可直接回复喵~
            """
            reason = "reason"
            param = {"#reason#": reason}
            phonenumber = 6666666
            tpl_send_sms(apikey=APPKEY, tpl_id=SMS_TEMPLATE_CODE_PROBLEM, tpl_value=param, mobile=phonenumber)
            pass
        # 其他情况直接pass就好,不需要发短信
        else:
            pass


