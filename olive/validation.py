from urllib.parse import urlparse


class Validation:
    def __init__(self):
        pass

    @staticmethod
    def is_url_valid(url, required_parts=['scheme', 'netloc']):
        url_parts = urlparse(url)
        for part in required_parts:
            if not getattr(url_parts, part):
                return False
        return True
