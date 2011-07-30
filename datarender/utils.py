from django.utils.datastructures import SortedDict


class ObjectCounterMetaclass(type):
    """
    ObjectCounterMetaclass provides way to create class
    with creation counter that doesn't need to invoke
    __init__ method.
    """

    # creation_counter variable on each ObjectCounter
    # subclass works like global 'high water mark'
    creation_counter = 0

    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.creation_counter = ObjectCounterMetaclass.creation_counter
        ObjectCounterMetaclass.creation_counter += 1
        return obj


class ObjectCounter(object):
    """
    Base class that provides creation_counter attibute
    and counts objects that derives from it.

    >>> class Countable(ObjectCounter):
    >>>     pass
    >>>
    >>> assert Countable().creation_counter == 0
    >>> assert Countable().creation_counter == 1
    >>> assert Countable().creation_counter == 2
    """
    __metaclass__ = ObjectCounterMetaclass


def collect_items(dictionary, item_class):
    result = [(name, dictionary.pop(name))
              for name, obj in dictionary.items()
              if isinstance(obj, item_class)]
    result.sort(key=lambda i : i[1].creation_counter)
    return result


def collect_attribute(attr_name, objects, filterfun=lambda attr: attr is not None):
    result = []
    for obj in objects:
        attr = getattr(obj, attr_name, None)
        if filterfun(attr):
            result.append(attr)
    return result


def pretty_name(name):
    return ' '.join(name.split('_')).capitalize()
