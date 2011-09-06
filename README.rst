datarender
==========

Datarender is reusable django application that gives ability
to render objects details in more generic way.


Usage
-----

Let's follow by simple example. Assuming we've got
sample "tasks" application that uses the following model:


::

    # tasks.models
    from django.db import models

    class Task(models.Model):
        title = models.CharField(max_length=512)
        description = models.TextField(null=True, blank=True)
        close_date = models.DateTimeField(null=True, blank=True)


Suppose we want to render it in template, for example in detail
view of task object. The simplest usage of datarender plugin is just
point fields you want to show:


::

    <table>
        {% for value, f in task|object_fields:"title,description,close_date" %}
        <tr>
            <td class="label-{{ f.meta.css }}">{{ f.meta.label }}</td>
     	    <td class="{{ f.meta.css }">{% render value f %}</td>
        </tr>
        {% endfor %}
    </table>


datarender plugin will simply create generic fields for a given
model instance. That's all you need for a basic usage.
