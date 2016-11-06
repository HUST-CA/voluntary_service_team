import urllib.request
import urllib.parse
import http.client
import csv
# 服务地址
sms_host = "sms.yunpian.com"
voice_host = "voice.yunpian.com"
# 端口号
port = 443
# 版本号
version = "v2"

# 模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_single_send.json"

def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    """
    模板接口发短信
    """
    encoded_tpl_value = urllib.parse.urlencode(tpl_value)
    params = urllib.parse.urlencode(
        {'apikey': apikey, 'tpl_id': tpl_id, 'tpl_value': encoded_tpl_value, 'mobile': mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPSConnection(sms_host, port, timeout=30)
    conn.request("POST", sms_tpl_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read().decode()
    conn.close()
    return response_str

    #tpl_value = {'#name#': stuname, '#time#':'11月5日（明晚）7点','#locate#':'东九楼B201','#type#':'视频制作','#code#':'不用点链接','#times#':'1'}
        #print(mobile)
    #print(tpl_send_sms(apikey, tpl_id, tpl_value, mobile))
        # 调用模板接口发语音短信
        # print send_voice_sms(apikey,voiceCode,mobile)
