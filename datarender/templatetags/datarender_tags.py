# -*- coding: utf-8 -*-
from django import template
from django.utils.importlib import import_module

from datarender import DynamicFieldSet

register = template.Library()


def render(tf):
    return tf._fieldset.render(tf.meta, tf._fieldset.get(tf.meta, tf._data))
register.simple_tag(render)


def fields(data, fieldset):
    """
    ``fieldset`` can be FieldSet subclass instance or
    string with comma separated field names
    """
    if isinstance(fieldset, basestring):
        fieldset = DynamicFieldSet(data.__class__, fieldset.split(","))
    return fieldset.iterate(data)
register.filter(fields)


class RendererNode(template.Node):
    def __init__(self, fieldset_path, var_name, param_name=None):
        self.fieldset_path = fieldset_path.strip('"\'')
        self.var_name = var_name.strip('"\'')
        self.param_name = param_name

    def _get_constructor_param(self, context):
        if self.param_name is None:
            return None

        try:
            return template.Variable(self.param_name.strip('"\'')).resolve(context)
        except template.VariableDoesNotExist:
            return None

    def _get_fieldset_class(self):
        path = list(self.fieldset_path.split("."))

        class_name = path[-1]    # last element should be class name
        module_path = path[:-1]  # there should be path to the class

        render_module = import_module(".".join(module_path))
        return getattr(render_module, class_name)

    def render(self, context):
        FieldSetClass = self._get_fieldset_class()
        context[self.var_name] = FieldSetClass(self._get_constructor_param(context))
        return u''


def renderer(parser, token):
    """{% renderer myapp.FancyFieldSet [param] as fielset_instance_name %}"""

    parts = token.split_contents()
    parts_len = len(parts)

    if parts_len == 4:  # no "param"
        return RendererNode(fieldset_path=parts[1], var_name=parts[3])
    if parts_len == 5:  # there is param
        return RendererNode(fieldset_path=parts[1], var_name=parts[4], param_name=parts[2])

    raise template.TemplateSyntaxError(
        "'fieldset' tag must be of the form: {% renderer myapp.MyFancyFieldSet [param] as fielset_instance_name %}")

register.tag(renderer)
