import urllib.request
import urllib.parse
import http.client
import threading
import json

from voluntary_service_team.secure_settings import APIKEY


class SMS:
    def __init__(self, **kwargs):
        # apikey.可在官网（http://www.yuanpian.com)登录后获取
        self.apikey = kwargs['apikey']
        # 短信内容
        self.text = kwargs['text']
        # 接收者手机号
        self.mobile = kwargs['mobile']
        # template_id
        self.tpl_id = kwargs['tpl_id']
        # template_value
        self.tpl_value = kwargs['tpl_value']

        # 服务地址
        self.sms_host = "sms.yunpian.com"
        self.voice_host = "voice.yunpian.com"
        # 端口号
        self.port = 443
        # 版本号
        self.version = "v2"
        # 查账户信息的URI
        self.user_get_uri = "/" + self.version + "/user/get.json"
        # 智能匹配模板短信接口的URI
        self.sms_send_uri = "/" + self.version + "/sms/single_send.json"
        # 模板短信接口的URI
        self.sms_tpl_send_uri = "/" + self.version + "/sms/tpl_single_send.json"
        # 语音短信接口的URI
        self.sms_voice_send_uri = "/" + self.version + "/voice/send.json"
        # 语音验证码
        self.voiceCode = 1234

    def get_user_info(self):
        """
        取账户信息
        """
        conn = http.client.HTTPSConnection(self.sms_host, self.port)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        params = urllib.parse.urlencode({'apikey': self.apikey})
        conn.request('POST', self.user_get_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read().decode()
        conn.close()
        return response_str

    def send_sms(self):
        """
        只传text,发短信内容就是text内容
        """
        params = urllib.parse.urlencode({'apikey': self.apikey, 'text': self.text, 'mobile': self.mobile})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPSConnection(self.sms_host, self.port, timeout=30)
        conn.request("POST", self.sms_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read().decode()
        conn.close()
        return response_str

    def tpl_send_sms(self):
        """
        传模板id和模板变量,发短信内容是经过变量渲染后的模板
        """
        encoded_tpl_value = urllib.parse.urlencode(self.tpl_value)
        params = urllib.parse.urlencode(
            {'apikey': self.apikey, 'tpl_id': self.tpl_id, 'tpl_value': encoded_tpl_value, 'mobile': self.mobile})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPSConnection(self.sms_host, self.port, timeout=30)
        conn.request("POST", self.sms_tpl_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read().decode()
        conn.close()
        return response_str

# 封装成线程比较好
# class SMSThread(threading.Thread):
#     def __init__(self):
#         pass
#
#     def run(self):
#         pass


if __name__ == '__main__':
    # 作为测试
    kwargs = dict()
    kwargs['apikey'] = APIKEY
    kwargs['text'] = "【计算机协会】#type#学习小组将于#time#在#locate#进行第#times#授课，欢迎你来参加哦~收到请点击确认：huca.tech/#code#"
    kwargs['mobile'] = "15927554193"
    kwargs['tpl_id'] = 1599182
    kwargs['tpl_value'] = {'#type#': '视频制作', '#time#': '今晚', '#locate#': '东九ac', '#times#': '1', '#code#': 'aafb'}
    sms = SMS(**kwargs)
    sms.get_user_info()  # 测试获取用户信息
    sms.tpl_send_sms()  # 测试发送模板短信
