"""
Usage:

x = getattr(importlib.import_module("qeda.verbose", "true/false"), "true/false")
x('string')
"""


def true(*args, **kwargs):
    for arg in args:
        print(arg,)
    for kwarg in kwargs:
        print(kwarg,)


false = lambda *a: None
