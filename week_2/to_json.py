import json
import functools


def to_json(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        return json.dumps(result)
    return wrapped
#
#
# @to_json
# def mul(*args, **kwargs):
#     return kwargs
#
# print(mul(a=1, b=2, c=3))
