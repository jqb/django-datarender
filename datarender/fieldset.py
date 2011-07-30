# -*- coding: utf-8 -*-
from datarender.utils import SortedDict
from datarender.options import Options
from datarender.models import FieldSetMetaclass
from datarender.fields import Header, HeaderMapper, FormField, FormFieldMapper


class TemplateField(object):
    # just the runtime representation for template usage

    def __init__(self, fieldset, field):
        self.fieldset = fieldset
        self.meta = field


class BaseFieldSet(object):
    runtime_field = TemplateField

    def __init__(self, runtime_data=None):
        self.runtime_data = runtime_data

    def get(self, fieldmeta, obj):
        get_attr = getattr(self, 'get_%s' % fieldmeta.name, None)
        if get_attr:
            return get_attr(obj)
        return fieldmeta.get(obj, self.runtime_data)

    def render(self, fieldmeta, obj):
        render_attr = getattr(self, 'render_%s' % fieldmeta.name, None)
        if render_attr:
            return render_attr(obj)
        return fieldmeta.render(obj, self.runtime_data)

    def iterate(self, data):
        result = []
        for fieldmeta in self.base_fields.values():
            result.append((self.get(fieldmeta, data), self.runtime_field(self, fieldmeta)))
        return result


class DynamicFieldSet(BaseFieldSet):
    def __init__(self, model_class, field_names, runtime_data=None):
        self.base_fields = SortedDict()
        self._meta = opts = Options.from_dict({
                'model': model_class,
                'fields': field_names,
                })

        for field in model_class._meta.fields:
            if field.name in field_names:
                new_field = opts.field_mapper.get(field)
                new_field.name = field.name
                self.base_fields[field.name] = new_field

        super(DynamicFieldSet, self).__init__(runtime_data)


class FieldSet(BaseFieldSet):
    __metaclass__ = FieldSetMetaclass


class HeaderSet(FieldSet):
    class Meta:
        field_class = Header
        field_mapper = HeaderMapper()


class ColumnSet(FieldSet):
    headerset_class = None

    def _get_headerset(cls):
        """
        if ``headerset_class`` is defined it returns
        an instance of ``headerset_class``.
        Else it creates subclass of HeaderSet on fly.
        """
        if cls.headerset_class is None:
            class _HeaderSet(HeaderSet):
                class Meta:
                    model = cls._meta.model
                    form = cls._meta.form
                    exclude = cls._meta.exclude
                    fields = cls._meta.fields

            cls.headerset_class = _HeaderSet

            for key in cls.base_fields.keys():
                if key not in cls.headerset_class.base_fields:
                    header = Header()
                    header.name = key
                    cls.headerset_class.base_fields[key] = header

        return cls.headerset_class
    headerset = classmethod(_get_headerset)

    def headers(self):
        headerset_class = self.headerset()
        return headerset_class(self.runtime_data).iterate(self._meta)


class FormFieldSet(FieldSet):
    class Meta:
        field_class = FormField
        field_mapper = FormFieldMapper()
