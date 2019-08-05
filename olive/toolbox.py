from olive.exc import PythonStackNotSupported
from marshmallow import fields
import datetime
import inspect


def get_caller_name(calframe_num=2):
    """
    :param calframe_num: used to get method name in different call levels
    :return: caller method name
    """

    # CPython implementation detail of inspect.currentframe():
    #     This function relies on Python stack frame support in the interpreter,
    #     which isn’t guaranteed to exist in all implementations of Python.
    #     If running in an implementation without Python stack frame support,
    #     this function returns None.
    curframe = inspect.currentframe()
    if curframe is None:
        raise PythonStackNotSupported

    try:
        # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
        calframe = inspect.getouterframes(curframe, 2)
        caller_name = calframe[calframe_num][3]
    finally:
        del curframe

    return caller_name


# This is a workaround you can read more here:
#     - https://github.com/marshmallow-code/marshmallow/issues/656#issuecomment-318587611
class MarshmallowDateTimeField(fields.DateTime):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime.datetime):
            return value
        return super()._deserialize(value, attr, data)
