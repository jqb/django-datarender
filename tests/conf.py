DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'project.db',
        }
    }

INSTALLED_APPS = (
    'datarender',
    'tests',
    'tests.tasks',
    )
