from testapps.tasks import models
from django import forms


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
