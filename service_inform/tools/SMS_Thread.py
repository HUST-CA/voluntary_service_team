import threading

from .send_sms import SMS
from voluntary_service_team.secure_settings import APIKEY
from voluntary_service_team.secure_settings import TPL_ID


class SMSThread(threading.Thread):
    def __init__(self, receiver_mobile, status=None, **kwargs):
        super(SMSThread, self).__init__()
        self.daemon = False
        if status == '收到':
            self.name = '【收到】' + receiver_mobile
            '''
            模板内容：【华科计算机协会】亲~你的电脑我们已经收到啦！提取码：#code1#，戳 https://huca.tech/#code# 可以查看维修进度哦~
            '''
            self.params = {'apikey': APIKEY,
                           'tpl_id': TPL_ID['receive'],
                           'tpl_value': {"#code#": kwargs['short_link'], "#code1#": kwargs['serial_number']},
                           'mobile': receiver_mobile}
        elif status == '完成':
            self.name = '【完成】' + receiver_mobile
            """
            【华科计算机协会】亲亲亲！普天同庆！你的电脑已经维修完成啦！
            请凭 #code# 提取电脑哦！
            https://huca.tech/#code1#
            """
            # 注意：这里 code1 是短链接，code 是取货号，而上面一条反过来。
            # 请自行找 PM 解决
            self.params = {'apikey': APIKEY,
                           'tpl_id': TPL_ID['finish'],
                           'tpl_value': {"#code1#": kwargs['short_link'], "#code#": kwargs['serial_number']},
                           'mobile': receiver_mobile}
        elif status == '遇到问题需反馈':
            self.name = '【遇到问题】' + receiver_mobile
            """
            【华科计算机协会】亲~维修出现了问题嚎。原因：#reason#
            本短信可直接回复喵~
            """
            self.params = {'apikey': APIKEY,
                           'tpl_id': TPL_ID['trouble'],
                           'tpl_value': {"#reason#": kwargs['reason']},
                           'mobile': receiver_mobile}
        else:
            pass  # for more utility

    def run(self):
        print(self.name + ' is running...')
        SMS(**self.params).tpl_send_sms()
