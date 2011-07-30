# -*- coding: utf-8 -*-
from operator import attrgetter, itemgetter

from django.test import TestCase
from django.utils.datastructures import SortedDict

from testapps.tasks.models import Task
from testapps.tasks.render import (
    TaskList, TaskListNoID, TaskListHeader,
    TaskFormFieldSet)

import datarender

from datarender import Field
from datarender.utils import collect_items, collect_attribute


class DatarenderFieldTest(TestCase):
    def setUp(self):
        self.first_field = datarender.Field().creation_counter

    def test_datarender_fields_instances_are_countable(self):
        self.assertEquals(datarender.Field().creation_counter, self.first_field + 1)
        self.assertEquals(datarender.Field().creation_counter, self.first_field + 2)
        self.assertEquals(datarender.Field().creation_counter, self.first_field + 3)

        self.assertEquals(datarender.DateField().creation_counter, self.first_field + 4)
        self.assertEquals(datarender.DateField().creation_counter, self.first_field + 5)
        self.assertEquals(datarender.DateField().creation_counter, self.first_field + 6)

        self.assertEquals(datarender.Header().creation_counter, self.first_field + 7)
        self.assertEquals(datarender.Header().creation_counter, self.first_field + 8)
        self.assertEquals(datarender.Header().creation_counter, self.first_field + 9)


class GeneratingFieldSetForModel(TestCase):
    def test_tasklist_fieldset_class_has_base_field_attribute(self):
        assert hasattr(TaskList, 'base_fields')

    def test_tasklist_fieldset_meta_attr_has_default_object_that_maps_the_fields(self):
        assert hasattr(TaskList._meta, 'field_mapper')

    def test_tasklist_fieldset_meta_field_mapper_attr_can_be_overriden(self):
        assert hasattr(TaskList._meta, 'field_mapper')

    def test_base_fields_is_instance_of_sorted_dict(self):
        assert isinstance(TaskList.base_fields, SortedDict)

    def test_base_fields_contains_all_generated_fields_for_task_model(self):
        field_names = map(attrgetter('name'), Task._meta.fields)
        for fname in field_names:
            error_msg = 'No "%s" field, Task.base_fields: %s' % (fname, TaskList.base_fields)
            assert fname in TaskList.base_fields, error_msg

    def test_base_fields_not_contains_fields_listed_in_exclude_option(self):
        excluded = ['id']
        for fname in excluded:
            error_msg = 'Field "%s" shouldn\'t be in Task.base_fields: %s' % (fname, TaskList.base_fields)
            assert fname not in TaskListNoID.base_fields, error_msg


class UtilsTest(TestCase):

    class Person(object):
        def __init__(self, name):
            self.name = name

    def setUp(self):
        self.attrs = {
            'title': 'Wrong title class',
            'project': Field(),     # creation counter n + 1
            'description': Field(), # creation counter n + 2
            'status': Field()       # creation counter n + 3
            }

    def test_collect_items_pops_items_that_are_instance_of_given_class(self):
        attrs = SortedDict(collect_items(self.attrs, Field))

        for key in ['project', 'description', 'status']:
            assert key in attrs

        for key in ['title']:
            assert key not in attrs

    def test_collect_items_sort_the_results(self):
        expected = ['project', 'description', 'status']
        result = map(itemgetter(0), collect_items(self.attrs, Field))
        self.assertEquals(expected, result)

    def test_collect_attribute_collects_attributes_of_the_given_name_of_given_objects_list(self):
        Person = UtilsTest.Person

        expected = ['john', 'malcolm', 'sara', 'ted']
        result = collect_attribute('name', [Person('john'), Person('malcolm'),
                                            Person('sara'), Person('ted')])
        self.assertEquals(expected, result)

    def test_collect_attribute_ommits_attributes_with_value_None(self):
        Person = UtilsTest.Person

        expected = ['john', 'malcolm', 'sara', 'ted']
        result = collect_attribute('name', [Person('john'), Person('malcolm'), Person(None),
                                            Person('sara'), Person(None), Person('ted')])
        self.assertEquals(expected, result)


class HeaderFieldSetTest(TestCase):
    def test_field_class_is_header(self):
        headers = TaskListHeader.base_fields.values()
        msg = "not all are the Header class: %s" % headers
        assert all(map(lambda h: h.__class__ == datarender.Header, headers)), msg


class GeneratingFormFieldSetForModel(TestCase):
    def test_tasklist_fieldset_class_has_base_field_attribute(self):
        assert hasattr(TaskFormFieldSet, 'base_fields')

    def test_tasklist_fieldset_meta_attr_has_default_object_that_maps_the_fields(self):
        assert hasattr(TaskFormFieldSet._meta, 'field_mapper')

    def test_tasklist_fieldset_meta_field_mapper_attr_can_be_overriden(self):
        assert hasattr(TaskFormFieldSet._meta, 'field_mapper')

    def test_base_fields_is_instance_of_sorted_dict(self):
        assert isinstance(TaskFormFieldSet.base_fields, SortedDict)

    def test_base_fields_contains_all_generated_fields_for_task_form(self):
        field_names = map(attrgetter('name'), Task._meta.fields)
        field_names.pop(field_names.index('id'))  # no 'id' field
        for fname in field_names:
            error_msg = 'No "%s" field, Task.base_fields: %s' % (fname, TaskFormFieldSet.base_fields)
            assert fname in TaskFormFieldSet.base_fields, error_msg

    def test_base_fields_not_contains_fields_listed_in_exclude_option(self):
        excluded = ['id']
        for fname in excluded:
            error_msg = 'Field "%s" shouldn\'t be in Task.base_fields: %s' % (fname, TaskFormFieldSet.base_fields)
            assert fname not in TaskFormFieldSet.base_fields, error_msg
