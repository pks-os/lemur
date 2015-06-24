"""
.. module: lemur.extensions
    :copyright: (c) 2015 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
"""

from flask.ext.sqlalchemy import SQLAlchemy, SignallingSession, SessionBase


class _SignallingSession(SignallingSession):
    """A subclass of `SignallingSession` that allows for `binds` to be specified
    in the `options` keyword arguments.

    """
    def __init__(self, db, autocommit=False, autoflush=True, **options):
        self.app = db.get_app()
        self._model_changes = {}
        self.emit_modification_signals = \
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS']

        bind = options.pop('bind', None)
        if bind is None:
            bind = db.engine

        binds = options.pop('binds', None)
        if binds is None:
            binds = db.get_binds(self.app)

        SessionBase.__init__(self,
                             autocommit=autocommit,
                             autoflush=autoflush,
                             bind=bind,
                             binds=binds,
                             **options)


class _SQLAlchemy(SQLAlchemy):
    """A subclass of `SQLAlchemy` that uses `_SignallingSession`."""
    def create_session(self, options):
        return _SignallingSession(self, **options)

db = SQLAlchemy()

from flask.ext.migrate import Migrate
migrate = Migrate()

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask.ext.principal import Principal
principal = Principal()

