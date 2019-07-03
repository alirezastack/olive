from uuid import uuid4


class Authentication:
    def __init__(self):
        pass

    def generate_token(self, prefix):
        return '{}:{}'.format(prefix, uuid4().hex)
