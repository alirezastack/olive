from olive.exc import PythonStackNotSupported
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
