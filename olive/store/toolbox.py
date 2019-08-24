from olive.exc import InvalidObjectId
from bson import ObjectId
from marshmallow import fields, missing, Schema, post_dump
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


def int_to_object_id(identifier, to_str=True):
    s = str(identifier)
    s = '0' * (24 - len(s)) + s
    if to_str:
        return s

    return bson.ObjectId(s)


class MongoObjectId(fields.Field):
    def serialize(self, attr, obj, accessor=None, **kwargs):
        if attr in obj:
            return str(obj[attr])
        else:
            return None

    def deserialize(self, value, attr=None, data=None, **kwargs):
        if value is missing:
            return None
        return str(value)


class BaseSchema(Schema):
    def __init__(self, id_field='_id', exclude_none_id=False, *args, **kwargs):
        super(BaseSchema, self).__init__(*args, **kwargs)
        self.id_field = id_field
        self.exclude_none_id = exclude_none_id

    @post_dump
    def clean_dumped_id(self, data, *args, **kwargs):
        if self.exclude_none_id and self.id_field in data and data[self.id_field] is None:
            del data[self.id_field]
        return data
