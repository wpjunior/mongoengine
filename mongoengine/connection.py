from pymongo import Connection
import multiprocessing
import threading

__all__ = ['ConnectionError', 'connect']


_connection_defaults = {
    'host': 'localhost',
    'port': 27017,
}
_connection = {}
_connection_settings = _connection_defaults.copy()
_databases = {}

_db_name = None
_db_username = None
_db_password = None
_db = {}


class ConnectionError(Exception):
    pass


def _get_connection(reconnect=False):
    """Handles the connection to the database
    """
    global _connection
    identity = get_identity()
    # Connect to the database if not already connected
    if _connection.get(identity) is None or reconnect:
        try:
            _connection[identity] = Connection(**_connection_settings)
        except Exception, e:
            raise ConnectionError("Cannot connect to the database:\n%s" % e)
    return _connection[identity]

def _get_db(db_name=None, reconnect=False):
    """Handles database connections and authentication based on the current
    identity

    db_name: if None use default database used in connect
    """
    global _db, _connection, _databases
    identity = get_identity()

    # Connect if not already connected
    if _connection.get(identity) is None or reconnect:
        _connection[identity] = _get_connection(reconnect=reconnect)

    # alternative database
    if db_name:
        if _databases.get(db_name) is None:
            _databases[db_name] = {}

        if _databases[db_name].get(identity) is None or reconnect:
            _databases[db_name][identity] = _connection[identity][db_name]
    
            if _db_username and _db_password:
                _databases[db_name][identity].authenticate(
                    _db_username, _db_password)

        return _databases[db_name][identity]

    # default database
    if _db.get(identity) is None or reconnect:
        # _db_name will be None if the user hasn't called connect()
        if _db_name is None:
            raise ConnectionError('Not connected to the database')

        # Get DB from current connection and authenticate if necessary
        _db[identity] = _connection[identity][_db_name]
        if _db_username and _db_password:
            _db[identity].authenticate(_db_username, _db_password)

    return _db[identity]

def get_identity():
    """Creates an identity key based on the current process and thread
    identity.
    """
    identity = multiprocessing.current_process()._identity
    identity = 0 if not identity else identity[0]

    identity = (identity, threading.current_thread().ident)
    return identity

def connect(db, username=None, password=None, **kwargs):
    """Connect to the database specified by the 'db' argument. Connection
    settings may be provided here as well if the database is not running on
    the default port on localhost. If authentication is needed, provide
    username and password arguments as well.
    """
    global _connection_settings, _db_name, _db_username, _db_password, _db
    _connection_settings = dict(_connection_defaults, **kwargs)
    _db_name = db
    _db_username = username
    _db_password = password
    return _get_db(reconnect=True)

