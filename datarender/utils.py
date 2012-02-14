from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext

from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.template import Context, Template


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


class RenderingMixin(object):
    def render_to_string(self, *args, **kwargs):
        return render_to_string(*args, **kwargs)

    def mark_safe(self, *args, **kwargs):
        return mark_safe(*args, **kwargs)

    def render_template(self, template_string, context):
        return unicode(Template(template_string).render(Context(context)))

    def pretty_name(self, name, translate=True):
        if translate:
            return ugettext(pretty_name(name))
        return pretty_name(name)


class cached_property(object):
    """
    Defines property with cache field.

    >>> class Data(object):
    >>>     name = cached_property('_name', default=lambda self: 'default_name')
    >>>
    >>> data = Data()
    >>> print data.name
    >>> "default_name"
    >>> print data._name  # <= real value
    >>>
    """
    def __init__(self, target, default=lambda instance: None):
        self.name = target
        self.default_value = default

    def __get__(self, instance, type_instance):
        if instance is None:
            raise AttributeError('%s attribute can be get only on instance' % self.name)

        if not hasattr(instance, self.name):
            setattr(instance, self.name, self.default_value(instance))

        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)
