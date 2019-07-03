from uuid import uuid4


class Authentication:
    def __init__(self):
        pass

    @staticmethod
    def generate_token(prefix):
        return '{}:{}'.format(prefix, uuid4().hex)
