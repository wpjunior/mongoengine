import unittest
from mongoengine import *
from mongoengine.connection import _get_db
from mongoengine import serializers

class SerializersTest(unittest.TestCase):
    def setUp(self):
        connect(db='mongoenginetest')
        self.db = _get_db()

    def test_basic_serialization(self):
        class Person(Document):
            name = StringField()
            age = IntField()

        Person(name="Wilson", age=18).save()

        def raising():
            data = serializers.serialize("jsona",
                                         Person.objects.all())

        self.assertRaises(serializers.SerializerNotFound,
                          raising)

        data = serializers.serialize("python",
                                     Person.objects.all())
