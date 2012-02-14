# -*- coding: utf-8 -*-
from django import forms

from datarender.utils import ObjectCounter, RenderingMixin, cached_property


class BaseField(ObjectCounter, RenderingMixin):
    accepted_attrs = ('css', 'style')
    name = None  # name is always injected via metaclass

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if name not in self.accepted_attrs:
                raise AttributeError("There's no such attribute on \"accepted_attrs\" list: %s" % name)
            setattr(self, name, value)

    def get(self, obj, runtime_data=None):
        return getattr(obj, self.name)

    def render(self, value, runtime_data=None):
        return value


class Field(BaseField):
    accepted_attrs = BaseField.accepted_attrs + ('label',)
    label = cached_property('_label', default=lambda self: self.pretty_name(self.name))


class BaseDateField(Field):
    accepted_attrs = Field.accepted_attrs + ('format',)

    def render(self, value, runtime_data=None):
        if value:
            return value.strftime(self.format)
        return value


class DateField(BaseDateField):
    format = '%Y-%m-%d'


class DateTimeField(BaseDateField):
    format = '%Y-%m-%d %H:%M'


class FieldMapper(object):
    classes = {}
    default_field_class = Field

    def __init__(self, classes=None, default_field_class=None):
        self.classes = classes or self.__class__.classes
        self.default_field_class = default_field_class or self.__class__.default_field_class

    def get(self, dbfield):
        class_ = self.classes.get(dbfield.__class__, self.default_field_class)
        return class_(css=dbfield.__class__.__name__.lower())


class Header(BaseField):
    accepted_attrs = BaseField.accepted_attrs + ('header',)
    header = cached_property('_header', default=lambda self: self.pretty_name(self.name))

    def get(self, model, runtime_data=None):
        return model

    def render(self, model, runtime_data=None):
        return self.header


class FormField(Field):
    def get(self, form, data=None):
        return form[self.name]

    def render(self, formfield, data=None):
        return unicode(formfield)
