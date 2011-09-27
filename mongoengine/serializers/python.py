from mongoengine.serializers.base import BaseSerializer

class Serializer(BaseSerializer):
    def start(self):
        self.objects = []

    def end(self):
        pass

    def start_dump_obj(self, obj):
        self._object_data = {}

    def end_dump_obj(self, obj):
        self.objects.append(
            {'cls': obj.__class__._class_name,
             'pk': str(obj.pk),
             'data': self._object_data})

        self._object_data = None

    def dump_field(self, obj, field):
        raise NotImplementedError

    def get_value(self):
        return self.objects
