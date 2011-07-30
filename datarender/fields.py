# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from django.template.loader import render_to_string
from django.template import Context, Template

from datarender.utils import ObjectCounter, pretty_name


class BaseField(ObjectCounter):
    name = None  # name is always injected via metaclass
    translate = True

    def __init__(self, css=None, style=None):
        self._css = css
        self.style = style

    def pretty_name(self, name):
        if self.translate:
            return ugettext(pretty_name(name))
        return pretty_name(name)

    def css(self):
        if self._css is not None:
            return self._css
        elif isinstance(self.__class__.css, basestring):
            return self.__class__.css
        return self.__class__.__name__.lower()

    def _set_css(self, css):
        self._css = css

    css = property(css, _set_css)

    # utility functions
    def render_to_string(self, *args, **kwargs):
        return render_to_string(*args, **kwargs)

    def mark_safe(self, *args, **kwargs):
        return mark_safe(*args, **kwargs)

    def render_template(self, template_string, context):
        return unicode(Template(template_string).render(Context(context)))
    # end of utility functions

    def get(self, obj, runtime_data=None):
        return getattr(obj, self.name)

    def render(self, value, runtime_data=None):
        return value


class Field(BaseField):
    def __init__(self, label=None, css=None, style=None):
        self.label = label
        super(Field, self).__init__(css=css, style=style)

    def _get_label(self):
        return self._label if self._label is not None else self.pretty_name(self.name)

    def _set_label(self, label):
        self._label = label

    label = property(_get_label, _set_label)


class BaseDateField(Field):
    format = None

    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop('format', None) or self.__class__.format
        super(BaseDateField, self).__init__(*args, **kwargs)

    def render(self, value, runtime_data=None):
        if value:
            return value.strftime(self.format)
        return value


class DateField(BaseDateField):
    format = '%Y-%m-%d'


class DateTimeField(BaseDateField):
    format = '%Y-%m-%d %H:%M'


class FieldMapper(object):
    classes = {
        models.DateField: DateField,
        models.DateTimeField: DateTimeField,
        }

    def get(self, dbfield):
        class_ = self.classes.get(dbfield.__class__, Field)
        return class_(css=dbfield.__class__.__name__.lower())


class Header(BaseField):
    def __init__(self, css=None, style=None, header=None):
        self.header = header
        super(Header, self).__init__(css=css, style=style)

    def _get_header(self):
        return self._header if self._header is not None else self.pretty_name(self.name)

    def _set_header(self, header):
        self._header = header

    header = property(_get_header, _set_header)

    def get(self, model, runtime_data=None):
        return model

    def render(self, model, runtime_data=None):
        return self.header


class HeaderMapper(FieldMapper):
    def get(self, dbfield):
        return Header(css=dbfield.__class__.__name__.lower())


class FormField(Field):
    def get(self, form, data=None):
        return form[self.name]

    def render(self, formfield, data=None):
        return unicode(formfield)


class FormFieldMapper(object):
    classes = {}

    def get(self, formfield):
        class_ = self.classes.get(formfield.__class__, FormField)
        return class_(css=formfield.__class__.__name__.lower())
