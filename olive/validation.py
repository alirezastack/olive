from urllib.parse import urlparse


class Validation:

    @staticmethod
    def is_url_valid(url, required_parts=['scheme', 'netloc']):
        url_parts = urlparse(url)
        for part in required_parts:
            if not getattr(url_parts, part):
                return False
        return True
