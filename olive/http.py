from olive.exc import FetchError, DocumentNotFound
import requests


class Request(object):
    def __init__(self, url, headers, app):
        self.url = url
        self.headers = headers
        self.app = app

        # Flask has logger
        if 'logger' in dir(app):
            self.app.log = app.logger

    def get(self):
        self.app.log.debug('getting data from zoodroom-backend: {}'.format(self.url))
        res = requests.get(url=self.url,
                           timeout=10,
                           headers=self.headers)

        self.app.log.info('status-code: {}'.format(res.status_code))
        if res.status_code != requests.codes.OK:
            if res.status_code == requests.codes.NOT_FOUND:
                raise DocumentNotFound('requested resource not found on the server')

            raise FetchError('Could not fetch resource, status-code: {}'.format(res.status_code))

        if res.json()['status'] != 200:
            raise FetchError

        self.app.log.info('zoodroom-backend response: {}'.format(res.json()))
        return res.json()['data']


def parse_get_args(request, numeric_args):
    numeric_args = numeric_args or []
    filters = dict(request.args)

    # numeric_params = ['skip', 'page_size', 'city', 'complex']
    for numeric_arg in numeric_args:
        if numeric_arg in filters:
            filters[numeric_arg] = int(filters[numeric_arg])

    return filters
