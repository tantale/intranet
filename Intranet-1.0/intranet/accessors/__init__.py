"""
:package: intranet.accessors
:date: 2013-09-07
:author: Laurent LAPORTE <sandlol2009@gmail.com>

Database accessors
"""
from intranet.model import DBSession
import sqlalchemy.exc
import transaction
import logging

LOG = logging.getLogger(__name__)


class RecordNotFoundError(StandardError):
    """
    Exception raised when a record is missing in the database. Wrong uid?...
    """

    def __init__(self, class_name, uid):
        msg_fmt = "Record #{uid} not found in {class_name} table!"
        err_msg = msg_fmt.format(class_name=class_name,
                                 uid=uid)
        super(RecordNotFoundError, self).__init__(err_msg)
        self.uid = uid


class BasicAccessor(object):
    def __init__(self, record_class, session=None):
        self.record_class = record_class
        self.class_name = self.record_class.__name__
        self.session = session or DBSession

    def _get_record(self, uid):
        if isinstance(uid, basestring):
            uid = int(uid)
        elif isinstance(uid, (tuple, list)):
            uid = map(int, uid)
        record = self.session.query(self.record_class).get(uid)
        if record is None:
            raise RecordNotFoundError(self.class_name, uid)
        return record

    def _get_record_list(self, filter_cond=None, order_by_cond=None):
        query = self.session.query(self.record_class)
        if filter_cond is not None:
            if isinstance(filter_cond, (tuple, list)):
                query = query.filter(*filter_cond)
            else:
                query = query.filter(filter_cond)
        if order_by_cond is not None:
            if isinstance(order_by_cond, (tuple, list)):
                query = query.order_by(*order_by_cond)
            else:
                query = query.order_by(order_by_cond)
        return query.all()

    def _insert_record(self, **kwargs):
        record = self.record_class(**kwargs)
        with transaction.manager:
            self.session.add(record)
        return record

    def _update_record(self, uid, **kwargs):
        with transaction.manager:
            record = self._get_record(uid)
            for key, value in kwargs.iteritems():
                setattr(record, key, value)
        return record

    def _delete_record(self, uid):
        old_record = self._get_record(uid)
        with transaction.manager:
            self.session.delete(old_record)
        return old_record

    def reorder_position(self, uid_list, delim=u'|'):
        """
        Reorder a list of records according to the UIDs list.

        :type uid_list: list[int] or unicode
        :param uid_list: List of UIDs
        :type delim: unicode
        :param delim: delimiter used to separate UIDs if ``uid_list`` is a string.
        """
        assert hasattr(self.record_class, "position")
        uid_list = map(int, uid_list.split(delim)) if isinstance(uid_list, unicode) else uid_list
        with transaction.manager:
            filter_cond = self.record_class.uid.in_(uid_list)
            record_list = self._get_record_list(filter_cond)
            record_dict = {record.uid: record for record in record_list}
            for position, uid in enumerate(uid_list, 1):
                record_dict[uid].position = position

    def edit_label_in_place(self, uid, label):
        """
        Edit a record label in place.
        """
        assert hasattr(self.record_class, "label")
        if label:
            self._update_record(uid, label=label)
            return dict(status=u'updated', label=label)
        else:
            old = self._delete_record(uid)
            return dict(status=u'deleted', label=old.label)
