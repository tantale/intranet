"""
:package: intranet.accessors
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>

Database accessors
"""
from intranet.model import DBSession
from sqlalchemy.exc import IntegrityError
import transaction
import logging


LOG = logging.getLogger(__name__)


class DuplicateFoundError(StandardError):
    """
    Exception raised when a attempt was made to create (or update)
    a duplicate record.
    """
    def __init__(self, class_name, **attrs):
        msg_fmt = "Can't create/update a {class_name} record: duplicate found!"
        err_msg = msg_fmt.format(class_name=class_name)
        super(DuplicateFoundError, self).__init__(err_msg)
        self.attrs = attrs


class BasicAccessor(object):

    def __init__(self, record_class, session=None):
        self.record_class = record_class
        self.session = session or DBSession

    def _get_record(self, uid):
        return self.session.query(self.record_class).get(int(uid))

    def _get_record_list(self, filter_cond=None, order_by_cond=None):
        if filter_cond is None:
            if order_by_cond is None:
                return (self.session.query(self.record_class)
                        .all())
            else:
                return (self.session.query(self.record_class)
                        .order_by(order_by_cond)
                        .all())
        else:
            if order_by_cond is None:
                return (self.session.query(self.record_class)
                        .filter(filter_cond)
                        .all())
            else:
                return (self.session.query(self.record_class)
                        .filter(filter_cond)
                        .order_by(order_by_cond)
                        .all())

    def _insert_record(self, **kwargs):
        record = self.record_class(**kwargs)
        try:
            self.session.add(record)
            transaction.commit()
        except IntegrityError:
            transaction.abort()
            raise DuplicateFoundError(self.record_class.__name__, **kwargs)
        except:
            transaction.abort()
            raise
        else:
            return record

    def _update_record(self, uid, **kwargs):
        record = self._get_record(uid)
        try:
            for key, value in kwargs.iteritems():
                setattr(record, key, value)
            transaction.commit()
        except IntegrityError:
            transaction.abort()
            raise DuplicateFoundError(self.record_class.__name__, **kwargs)
        except:
            transaction.abort()
            raise
        else:
            return record

    def _delete_record(self, uid):
        try:
            old_record = self._get_record(uid)
            self.session.delete(old_record)
            transaction.commit()
        except:
            transaction.abort()
            raise
        return old_record
