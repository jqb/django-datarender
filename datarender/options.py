from datarender.fields import FieldMapper, Field

class Options(object):
    def __init__(self, options, init=True):
        self.model = getattr(options, 'model', None)
        self.form = getattr(options, 'form', None)
        self.fields = getattr(options, 'fields', None)
        self.exclude = getattr(options, 'exclude', None)
        self.field_class = getattr(options, 'field_class', None)
        self.mapping = getattr(options, 'mapping', None)
        self.field_mapper = None

        if init:
            self.init()

    def init(self):
        self.field_mapper = FieldMapper(
            default_field_class=self.field_class,
            classes=self.mapping)

    @classmethod
    def from_dict(self, data):
        opts = Options(None, init=False)  # defaults
        for attr in ['model', 'form', 'fields', 'exclude', 'field_mapper', 'field_class']:
            if attr in data:
                setattr(opts, attr, data[attr])
        opts.init()
        return opts
