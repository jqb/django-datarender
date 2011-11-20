# -*- coding: utf-8 -*-
from operator import attrgetter, itemgetter

from django.test import TestCase
from django.utils.datastructures import SortedDict

from datarender.utils import collect_items, collect_attribute
from datarender import Field


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
