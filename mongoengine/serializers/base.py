__all__ = ['BaseSerializer']

try:
    # fast StringIO implemented in C
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class BaseSerializer(object):
    def start_dump_obj(self, obj):
        """
        Dumps a object
        """
        raise NotImplementedError

    def end_dump_obj(self):
        raise NotImplementedError

    def start(self):
        """
        start a serialization
        """
        raise NotImplementedError

    def end(self):
        """
        end a serialization
        """
        raise NotImplementedError

    def dump_field(self, obj, field):
        """
        Serialize a field
        """
        raise NotImplementedError

    def dump_extra_field(self, obj, name):
        """
        Serialize a extra argument
        """
        raise NotImplementedError

    def serialize(self, queryset, **options):
        """
        Serializes a queryset
        """

        self.options = options

        self.stream = options.pop("stream", StringIO())
        self.extras = options.pop('extras', ())
        self.fields = options.pop('fields', ())
        self.excludes = options.pop('excludes', ())

        self.start()

        for obj in queryset:
            self.start_dump_obj(obj)

            for field in obj._fields.itervalues():
                if field.name not in self.excludes:
                    if not self.fields or field.name in self.fields:
                        self.dump_field(obj, field)

            for extra in extras:
                self.dump_extra_field(obj, extra)

            self.end_dump_obj(obj)

        self.end()
