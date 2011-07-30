from datarender.fields import FieldMapper, Field

class Options(object):
    def __init__(self, options):
        self.model = getattr(options, 'model', None)
        self.form = getattr(options, 'form', None)
        self.fields = getattr(options, 'fields', None)
        self.exclude = getattr(options, 'exclude', None)
        self.field_mapper = getattr(options, 'field_mapper', FieldMapper())
        self.field_class = getattr(options, 'field_class', Field)

    @classmethod
    def from_dict(self, data):
        opts = Options(None)  # defaults
        for attr in ['model', 'form', 'fields', 'exclude', 'field_mapper', 'field_class']:
            if attr in data:
                setattr(opts, attr, data[name])
        return opts
