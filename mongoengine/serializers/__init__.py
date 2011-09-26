__all__ = ['serialize', 'SerializerNotFound', 'base']

import sys
from base import *

class SerializerNotFound(Exception):
    pass

LOADED_SERIALIZERS = {}

def load_serializer(fmt):
    """
    loads serializer
    """

    #try cache
    if fmt in LOADED_SERIALIZERS:
        return LOADED_SERIALIZERS[fmt]

    try:
        __import__("mongoengine.serializers.%s" % fmt)

        mod = sys.modules['mongoengine.serializers.%s' % fmt]
        serializer = getattr(mod, 'Serializer', None)
    except ImportError:
        serializer = None

    if serializer:
        #caching serializers
        LOADED_SERIALIZERS[fmt] = serializer
        return serializer
    else:
        raise SerializerNotFound

def serialize(fmt, queryset, **kwargs):
    cls_serializer = load_serializer(fmt)
    return cls_serializer().serialize(queryset,
                                      **kwargs)
