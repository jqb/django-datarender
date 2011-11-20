# -*- coding: utf-8 -*-
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=1024, null=True)
    description = models.TextField(null=True)
    close_date = models.DateTimeField(null=True)

    def is_closed(self):
        return self.close_date is not None

    def __unicode__(self):
        return '%s' % self.title
