import base64
import hashlib
import random

class ShortLink:
    def __init__(self, id):
        self.id = str(id).encode()

    def generate(self):
        b64_id = base64.b64encode(self.id).decode()
        short_link = b64_id.strip('=')
        return short_link


class SerialNumber:
    def __init__(self, id):
        self.id = id
        self.md5_gen = hashlib.md5()

    def generate(self):
        self.md5_gen.update(str(random.random() + self.id).encode())
        return ''.join(list(map(lambda x: str(x).zfill(3), self.md5_gen.digest()[0:2])))


if __name__ == '__main__':
    print('测试ShortLink', ShortLink(1).generate())
    print('测试SerialNumber', SerialNumber(1).generate())
