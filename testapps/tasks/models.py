# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    title = models.CharField(max_length=1024, null=True)
    description = models.TextField(null=True)

    def __unicode__(self):
        return '%s' % self.title


class Task(models.Model):
    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'

    project = models.ForeignKey(Project, null=True)
    reporter = models.ForeignKey(User, null=True, related_name='reported_tasks')
    owner = models.ForeignKey(User, null=True, related_name='owned_tasks')
    title = models.CharField(max_length=1024, null=True)
    description = models.TextField(null=True)

    creation_date = models.DateTimeField(null=True, default=lambda: datetime.now())
    deadline_date = models.DateField(null=True, default=lambda: datetime.now().date() + timedelta(days=1))
    close_date = models.DateTimeField(null=True)

    def is_assigned(self):
        return self.owner is not None

    def is_closed(self):
        return self.close_date is not None

    def __unicode__(self):
        return '%s' % self.title
