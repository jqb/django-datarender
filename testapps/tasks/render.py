# -*- coding: utf-8 -*-
from testapps.tasks.models import Task
from testapps.tasks.forms import TaskForm

import datarender


class TaskList(datarender.FieldSet):
    class Meta:
        model = Task


class TaskListNoID(datarender.FieldSet):
    class Meta:
        model = Task
        exclude = ('id',)


class TaskListHeader(datarender.HeaderSet):
    class Meta:
        model = Task


class TaskFormFieldSet(datarender.FormFieldSet):
    class Meta:
        form = TaskForm
        exclude = ('id',)
