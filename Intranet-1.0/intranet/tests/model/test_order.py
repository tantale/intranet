"""
:module: intranet.tests.model.test_order
:date: 2013-08-10
:author: Laurent LAPORTE <sandlol2009@gmail.com>

Test case of 'intranet.model.pointage.order' module.
"""
from intranet import model
from intranet.model import DBSession
from intranet.tests.model import ModelTest
from nose.tools import eq_
import datetime


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
        try:
            eq_(len(self.obj.order_phase_list), 0)
            for label in self.label_list:
                model.OrderPhase(self.obj, label)
            DBSession.flush()
        except:
            DBSession.rollback()
            raise

    def test_create_obj(self):
        """Order object can be created"""
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
            DBSession.flush()
        except:
            DBSession.rollback()
            raise
        order_phase_list = DBSession.query(model.OrderPhase).all()
        eq_(len(order_phase_list), 0)

    def test_delete_orphan(self):
        """Order phases orphans can be deleted"""
        try:
            order_phase = self.obj.order_phase_list[2]
            self.obj.order_phase_list.remove(order_phase)
            DBSession.flush()
        except:
            DBSession.rollback()
            raise
        order_phase_list = DBSession.query(model.OrderPhase).all()
        eq_(len(order_phase_list), len(self.label_list) - 1)

    def test_append_order_phase(self):
        """Order phases can be appended"""
        try:
            last_position = self.obj.order_phase_list[-1].position
            model.OrderPhase(self.obj, "New phase")
            DBSession.flush()
        except:
            DBSession.rollback()
            raise
        eq_(self.obj.order_phase_list[-1].position, last_position + 1)
