"""
:module: intranet.tests.model.test_order
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>

Test case of 'intranet.model.pointage.order' module.

To run this tests:
- activate the virtual environment and,
- run: 'nosetests -v intranet.tests.model.test_order'
"""
from intranet import model
from intranet.model import DBSession
from intranet.tests.model import ModelTest
from nose.tools import eq_
import datetime
import transaction
import logging


LOG = logging.getLogger(__name__)


class TestOrder(ModelTest):
    """
    Test case of 'Order' class.
    """

    klass = model.Order
    attrs = dict(order_ref="Order#1",
                 project_cat="yellow",
                 creation_date=datetime.date(2013, 8, 10),
                 close_date=datetime.date(2013, 9, 11))

    label_list = ["first", "second", "third", "last"]

    def setUp(self):
        super(TestOrder, self).setUp()
        # -- put Order in session
        self.obj = DBSession.query(model.Order).one()
        order_phase_list = DBSession.query(model.OrderPhase).all()
        eq_(len(order_phase_list), 0)
        try:
            for position, label in enumerate(self.label_list, 1):
                order_phase = model.OrderPhase(position, label)
                self.obj.order_phase_list.append(order_phase)
            transaction.commit()
        except:
            transaction.abort()
            raise
        order_phase_list = DBSession.query(model.OrderPhase).all()
        eq_(len(order_phase_list), len(self.label_list))

    def test_create_obj(self):
        """Order object can be created"""
        self.obj = DBSession.query(model.Order).one()
        for key, value in self.attrs.iteritems():
            eq_(getattr(self.obj, key), value)

    def test_query_obj(self):
        """Order objects can be queried"""
        for order in DBSession.query(self.klass).all():
            for key, value in self.attrs.iteritems():
                eq_(getattr(order, key), value)
            eq_(len(self.label_list), len(order.order_phase_list))
            for index, label in enumerate(self.label_list):
                order_phase = order.order_phase_list[index]
                eq_(order_phase.position, index + 1)
                eq_(order_phase.label, label)

    def test_delete_obj(self):
        """Order objects can be deleted"""
        try:
            DBSession.delete(self.obj)
            transaction.commit()
        except:
            transaction.abort()
            raise
        order_phase_list = DBSession.query(model.OrderPhase).all()
        eq_(len(order_phase_list), 0)

    def test_delete_orphan(self):
        """Order phases orphans can be deleted"""
        try:
            self.obj = DBSession.query(model.Order).one()
            order_phase = self.obj.order_phase_list[2]
            self.obj.order_phase_list.remove(order_phase)
            LOG.info("-- dirty: " + repr(DBSession.dirty))
            LOG.info("-- new: " + repr(DBSession.new))
            transaction.commit()
        except:
            transaction.abort()
            raise
        order_phase_list = DBSession.query(model.OrderPhase).all()
        eq_(len(order_phase_list), len(self.label_list) - 1)

    def test_append_order_phase(self):
        """Order phases can be appended"""
        try:
            self.obj = DBSession.query(model.Order).one()
            last_position = self.obj.order_phase_list[-1].position
            order_phase = model.OrderPhase(last_position + 1, "New phase")
            self.obj.order_phase_list.append(order_phase)
            LOG.info("-- dirty: " + repr(DBSession.dirty))
            LOG.info("-- new: " + repr(DBSession.new))
            transaction.commit()
        except:
            transaction.abort()
            raise
        order_phase_list = DBSession.query(model.OrderPhase).all()
        eq_(order_phase_list[-1].position, last_position + 1)
