from django.test import TestCase
from django.template import Context, Template

from tests.tasks.models import Task

import datarender


class SimplestUsageTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Test task", description="Test description")

    def render_template(self, template_string, context):
        return unicode(Template(template_string).render(Context(context)))

    def test_simplest_usage(self):
        template_string = ""
        template_string += """{% load datarender_tags %}"""
        template_string += """{% for value, f in task|object_fields:"title,description,close_date" %}"""
        template_string += """{{ f.meta.label }} | {% render value f %}"""
        template_string += "\n"
        template_string += """{% endfor %}"""

        result = self.render_template(template_string, {
                'task': self.task,
                })

        expected = ""
        expected += "Title | Test task"
        expected += "\n"
        expected += "Description | Test description"
        expected += "\n"
        expected += "Close date | None"
        expected += "\n"

        self.assertEquals(result, expected)
