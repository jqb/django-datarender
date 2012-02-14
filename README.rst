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
view of task object.


1) The simplest solution

The simplest  usage of datarender  plugin is just point  fields you
want to show

::

    {% load datarender_tags %}

    <div class="task-details">
        {% for value, f in task|fields:"title,description,close_date" %}
        <div class="field {{ f.meta.name }}">
            <div class="label">{{ f.meta.label }}</div>
     	    <div class="value">{% render value f %}</div>
        </tr>
        {% endfor %}
    </div>

datarender plugin will simply create generic fields for a given
model instance. That's all you need for a basic usage.


2) Using defined FieldSet class.

You can define rendering details in separate file.
datarender use "render.py" file in your application.

::

   # tasks.render
   from tasks.models import Task
   import datarender

   class TaskDetail(datarender.FieldSet):
       class Meta:
           model = Task


Once you define it in your_application.render file, you can simply use
it in the template

::

    {% load datarender_tags %}

    {% renderer "tasks.render.TaskDetail" as taskdetail %}

    {# you can add "runtime data" to the constructor, #}
    {# it can be everything eg. request object: #}
    {#     {% renderer "tasks.render.TaskDetail"  request as taskdetail %}   #}

    <div class="task-details">
        {% for f in task|fields:taskdetail %}
        <div class="field {{ f.meta.name }}">
            <div class="label">{{ f.meta.label }}</div>
     	    <div class="value">{% render f %}</div>
        </div>
        {% endfor %}
    </div>


Redering customization
----------------------

Once we'd created ``tasks.render`` module we can customize some
things:

1) ``exclude`` & ``fields`` meta options works as expected

2) we can redefine the way how specific field (eg. description) will
be rendered (eg. we want to transform description's rst to html using
imaginary ``rst_to_html_magic`` function)

::

   # tasks.render
   from tasks.models import Task
   import datarender


   class DescriptionDetail(datarender.Field):
       def render(self, description, data=None):
           return rst_to_html_magic(description)

   # the additional ``data`` param is just the ``runtime_data``
   # which can be passed to the constructor (or "renderer" tag in templates)

   class TaskDetail(datarender.FieldSet):
       class Meta:
           model = Task

       description = DescriptionDetail()


3) we can create our own additional field

::

   # tasks.render
   from tasks.models import Task
   import datarender


   class IsClosed(datarender.Field):
       def get(self, task, data=None):
           return task.is_closed()

       def render(self, isclosed, data=None):
           return "Closed" if isclosed else "Not closed"


   class TaskDetail(datarender.FieldSet):
       class Meta:
           model = Task

       is_closed = IsClosed()


Requirements
------------

- nosetest for tests
