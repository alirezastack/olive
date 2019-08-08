from olive.exc import InvalidObjectId
from bson import ObjectId
import traceback
import logging
import bson


def to_object_id(identifier):
    try:
        object_id = ObjectId(identifier)
    except bson.errors.InvalidId:
        logging.error(traceback.format_exc())
        raise InvalidObjectId("objectId {} is not a valid object ID".format(identifier))

    return object_id
