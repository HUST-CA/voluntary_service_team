import base64
import random


class ShortLink:
    def __init__(self, id):
        self.id = str(id).encode()

    def generate(self):
        b64_id = base64.b64encode(self.id).decode()
        short_link = b64_id.strip('=')
        return short_link


class SerialNumber:
    def __init__(self, id, tel):
        self.id = str(id)
        self.tel = list(str(tel))

    def generate(self):
        serial_number_list = list(ShortLink(self.id).generate())+random.sample(self.tel, 4)
        random.shuffle(serial_number_list)
        return ''.join(serial_number_list)


if __name__ == '__main__':
    print('测试ShortLink', ShortLink('1').generate())
    print('测试SerialNumber', SerialNumber('1', '12345678901').generate())
