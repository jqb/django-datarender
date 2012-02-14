# -*- coding: utf-8 -*-
import os, sys
from os.path import join, pardir, abspath, dirname

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.conf'
sys.path.insert(0, abspath(join(dirname(__file__), pardir)))

# Test stuff
test_runner, old_config = None, None

def setup():
    global test_runner, old_config
    from django.test.simple import DjangoTestSuiteRunner
    test_runner = DjangoTestSuiteRunner()
    test_runner.setup_test_environment()
    old_config = test_runner.setup_databases()

def teardown():
    test_runner.teardown_databases(old_config)
    test_runner.teardown_test_environment()
# ##############################################################
