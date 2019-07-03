from olive.patterns import singleton
from pymongo import MongoClient


@singleton
class MongoConnection:
    def __init__(self, cfgs, app):
        self._app = app
        self._service = cfgs['appname']
        self._client = MongoClient(**cfgs)

        self._app.log.debug('connecting to {} mongoDB server...'.format(self._service))
        # The ismaster command is cheap and does not require auth.
        # ConnectionFailure/ServerSelectionTimeoutError will be raised if MongoDB is not reachable
        self._client.admin.command('ismaster')
        self._app.log.info('connected to {} mongoDB server...'.format(self._service))

    @property
    def service_db(self):
        # return current service database
        return getattr(self._client, self._service)

    def __str__(self):
        return self._service + ' -> {}'.format(self._client)
