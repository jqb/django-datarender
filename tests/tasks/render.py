# -*- coding: utf-8 -*-
from tests.tasks.models import Task
from tests.tasks.forms import TaskForm

import datarender


class TaskList(datarender.ColumnSet):
    class Meta:
        model = Task


class TaskListNoID(datarender.ColumnSet):
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
