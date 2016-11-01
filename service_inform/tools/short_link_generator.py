import base64


class ShortLink:
    def __init__(self, id):
        self.id = str(id).encode()

    def generate(self):
        b64_id = base64.b64encode(self.id).decode()
        short_link = b64_id.strip('=')
        return short_link


if __name__ == '__main__':
    print(ShortLink('1').generate())
