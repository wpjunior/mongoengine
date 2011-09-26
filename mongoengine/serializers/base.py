__all__ = ['BaseSerializer']

class BaseSerializer(object):
    def dump_obj(self, obj):
        """
        Dumps a object
        """
        raise NotImplemented

    def serialize(self, queryset, **kwargs):
        """
        Serializes a queryset
        """
        raise NotImplemented
        for obj in queryset:
            dump_data = self.dump_obj(obj)
