import hashlib

test_values = {
    "id": "2a70c6bb4f2845da816ea1bfe5732747",  # 唯一序列号
    "mobile": "15200000000",  # 回复短信的手机号
    "reply_time": "2014-03-17 22:55:21",  # 回复短信的时间
    "text": "收到了，谢谢！",  # 回复的短信内容
    "extend": "01",  # 您发送时传入的扩展子号，未申请扩展功能或者未传入时为空串
    "base_extend": "8888",  # 系统分配的扩展子号
    "_sign": "393d079e0a00912335adfe46f4a2e10f"  # 签名字段
}

test_apikey = '0000'


def sign_good(values, apikey):
    sign = values.pop('_sign')
    li_k_v = []
    for k, v in values.items():
        li_k_v.append((k, v))
    string = ''
    li_k_v.sort()
    for each in li_k_v:
        string += each[1]
        string += ','
    string += apikey
    encoded_string = string.encode('utf-8')
    md5 = hashlib.md5()
    md5.update(encoded_string)
    return True if sign == md5.hexdigest() else False


if __name__ == '__main__':
    print(sign_good(test_values, test_apikey))
