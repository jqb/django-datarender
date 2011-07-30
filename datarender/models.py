from django.core.exceptions import ImproperlyConfigured

from datarender.fields import Field, FieldMapper
from datarender.utils import collect_items, collect_attribute, SortedDict
from datarender.options import Options

def collect_meta_classes(bases):
    return collect_attribute('_meta', bases[::-1])


def collect_bases_fields(bases):
    return collect_attribute('base_fields', bases[::-1])


def merge_meta_attributes(meta_classes, Meta=None, exclude=()):
    if not meta_classes and not Meta:
        return None

    attrs = {}
    for meta in meta_classes:
        attrs.update(meta.__dict__)

    # let's remove things that we don't want to inherit
    for fname in exclude:
        if fname in attrs:
            del attrs[fname]
    if Meta:
        attrs.update(Meta.__dict__)
    return type.__new__(type, 'Meta', (), attrs)


def should_be_excluded(name, fields, exclude):
    return bool((fields and not name in fields) or (exclude and name in exclude))


class FieldSetMetaclass(type):
    def __new__(cls, cls_name, bases, attrs):
        super_new = super(FieldSetMetaclass, cls).__new__

        # first proccess meta attribute
        meta_classes = collect_meta_classes(bases)
        Meta = attrs.get('Meta')
        Meta = merge_meta_attributes(meta_classes, Meta)
        opts = Options(Meta)

        if opts.model and opts.form:
            raise ImproperlyConfigured('You cannot setup "model" and "form" options at the same time')

        # extract user defined fields
        declared_fields = collect_items(attrs, opts.field_class)

        # bases_fields - each item of list is a 'base_fields' dict
        bases_fields = collect_bases_fields(bases)

        for base_fields in bases_fields:
            declared_fields = base_fields.items() + declared_fields

        # generating fields from model
        fields = []
        if opts.model:
            for dbfield in opts.model._meta.fields:
                if not should_be_excluded(dbfield.name, opts.fields, opts.exclude):
                    item = (dbfield.name, opts.field_mapper.get(dbfield))
                    fields.append(item)

        if opts.form:
            for name, formfield in opts.form.base_fields.items():
                if not should_be_excluded(name, opts.fields, opts.exclude):
                    item = (name, opts.field_mapper.get(formfield))
                    fields.append(item)

        fields = SortedDict(fields + declared_fields)

        # set the fields names
        for name, field in fields.items():
            field.name = name

        attrs['base_fields'] = fields
        attrs['_meta'] = opts
        new_class = super_new(cls, cls_name, bases, attrs)
        return new_class
