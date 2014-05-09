"""
:module: intranet.tests.model.test_cal_event_data
:date: 2013-09-17
:author: Laurent LAPORTE <sandlol2009@gmail.com>

"""
from intranet.model.pointage.employee import Employee
from intranet.model.pointage.order import Order
from intranet.model.pointage.order_phase import OrderPhase
import datetime

DEBUG = False

if DEBUG:
    from pprint import pprint


def parse_date(date_str):
    if date_str:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        return None


EMPLOYEE_LIST = [{u'employee_name': u'Bernard',
                  u'entry_date': u'1991-01-01',
                  u'exit_date': None,
                  u'photo_path': None,
                  u'uid': 2,
                  u'worked_hours': 39},
                 {u'employee_name': u'Ludovic',
                  u'entry_date': u'2004-07-01',
                  u'exit_date': u'2004-12-31',
                  u'photo_path': None,
                  u'uid': 5,
                  u'worked_hours': 39},
                 {u'employee_name': u'Nicolas',
                  u'entry_date': u'1990-01-01',
                  u'exit_date': None,
                  u'photo_path': u'/photo/pointage/employee/employee_1_1379445654.1.png',  # @IgnorePep8
                  u'uid': 1,
                  u'worked_hours': 39},
                 {u'employee_name': u'Thierry',
                  u'entry_date': u'1989-07-04',
                  u'exit_date': None,
                  u'photo_path': u'/photo/pointage/employee/employee_4_1379445753.43.png',  # @IgnorePep8
                  u'uid': 4,
                  u'worked_hours': 39},
                 {u'employee_name': u'\xc9lise',
                  u'entry_date': u'2000-05-11',
                  u'exit_date': None,
                  u'photo_path': u'/photo/pointage/employee/employee_3_1379445720.23.png',  # @IgnorePep8
                  u'uid': 3,
                  u'worked_hours': 31}]


def make_employee(record):
    return Employee(employee_name=record['employee_name'],
                    worked_hours=float(record['worked_hours']),
                    entry_date=parse_date(record['entry_date']),
                    exit_date=parse_date(record['exit_date']),
                    photo_path=record['photo_path'])

EMPLOYEE_LIST.sort(key=lambda record: record['uid'])
EMPLOYEE_LIST = map(make_employee, EMPLOYEE_LIST)

if DEBUG:
    map(pprint, EMPLOYEE_LIST)


ORDER_LIST = [{u'close_date': u'2013-02-15',
               u'creation_date': u'2013-01-02',
               u'order_phase_list': [{u'label': u'Avant-vente',
                                      u'order_uid': 1,
                                      u'position': 1,
                                      u'uid': 1},
                                     {u'label': u'Fabrication',
                                      u'order_uid': 1,
                                      u'position': 2,
                                      u'uid': 2},
                                     {u'label': u'Assemblage',
                                      u'order_uid': 1,
                                      u'position': 3,
                                      u'uid': 3},
                                     {u'label': u'Finition',
                                      u'order_uid': 1,
                                      u'position': 4,
                                      u'uid': 4},
                                     {u'label': u'Montage',
                                      u'order_uid': 1,
                                      u'position': 5,
                                      u'uid': 5}],
               u'order_ref': u'DUJARDIN - Cuisine',
               u'project_cat': u'colorCuisines',
               u'uid': 1},
              {u'close_date': u'2013-03-15',
               u'creation_date': u'2013-02-15',
               u'order_phase_list': [{u'label': u'Avant-vente',
                                      u'order_uid': 2,
                                      u'position': 1,
                                      u'uid': 6},
                                     {u'label': u'Fabrication',
                                      u'order_uid': 2,
                                      u'position': 2,
                                      u'uid': 7},
                                     {u'label': u'Assemblage',
                                      u'order_uid': 2,
                                      u'position': 3,
                                      u'uid': 8},
                                     {u'label': u'Finition',
                                      u'order_uid': 2,
                                      u'position': 4,
                                      u'uid': 9},
                                     {u'label': u'Livraison',
                                      u'order_uid': 2,
                                      u'position': 5,
                                      u'uid': 10}],
               u'order_ref': u'DUJARDIN - 6 Chaises',
               u'project_cat': u'colorMeubles',
               u'uid': 2},
              {u'close_date': u'2013-03-27',
               u'creation_date': u'2013-03-01',
               u'order_phase_list': [{u'label': u'Avant-Vente',
                                      u'order_uid': 3,
                                      u'position': 1,
                                      u'uid': 11},
                                     {u'label': u'Fabrication',
                                      u'order_uid': 3,
                                      u'position': 2,
                                      u'uid': 12},
                                     {u'label': u'Assemblage',
                                      u'order_uid': 3,
                                      u'position': 3,
                                      u'uid': 13},
                                     {u'label': u'Finition',
                                      u'order_uid': 3,
                                      u'position': 4,
                                      u'uid': 14},
                                     {u'label': u'Livraison',
                                      u'order_uid': 3,
                                      u'position': 5,
                                      u'uid': 15}],
               u'order_ref': u'LESCUILLER - 8 Chaises',
               u'project_cat': u'colorMeubles',
               u'uid': 3},
              {u'close_date': u'2013-05-21',
               u'creation_date': u'2013-05-15',
               u'order_phase_list': [{u'label': u'Avant-vente',
                                      u'order_uid': 4,
                                      u'position': 1,
                                      u'uid': 16},
                                     {u'label': u'Fabrication',
                                      u'order_uid': 4,
                                      u'position': 2,
                                      u'uid': 17},
                                     {u'label': u'Assemblage',
                                      u'order_uid': 4,
                                      u'position': 3,
                                      u'uid': 18},
                                     {u'label': u'Finition',
                                      u'order_uid': 4,
                                      u'position': 4,
                                      u'uid': 19},
                                     {u'label': u'Livraison',
                                      u'order_uid': 4,
                                      u'position': 5,
                                      u'uid': 20}],
               u'order_ref': u'PINSON - Bureau',
               u'project_cat': u'colorBureaux',
               u'uid': 4},
              {u'close_date': None,
               u'creation_date': u'2013-08-16',
               u'order_phase_list': [{u'label': u'Avant-vente',
                                      u'order_uid': 5,
                                      u'position': 1,
                                      u'uid': 22},
                                     {u'label': u'Fabrication',
                                      u'order_uid': 5,
                                      u'position': 2,
                                      u'uid': 21},
                                     {u'label': u'Assemblage',
                                      u'order_uid': 5,
                                      u'position': 3,
                                      u'uid': 23},
                                     {u'label': u'Finition',
                                      u'order_uid': 5,
                                      u'position': 4,
                                      u'uid': 24},
                                     {u'label': u'Livraison',
                                      u'order_uid': 5,
                                      u'position': 5,
                                      u'uid': 25}],
               u'order_ref': u'PINSON - Bureau (2)',
               u'project_cat': u'colorBureaux',
               u'uid': 5}]


def make_order(record):
    order = Order(order_ref=record['order_ref'],
                  project_cat=record['project_cat'],
                  creation_date=parse_date(record['creation_date']),
                  close_date=parse_date(record['close_date']))
    record['order_phase_list'].sort(key=lambda record: record['uid'])
    order_phase_list = [OrderPhase(position=record_phase['position'],
                                   label=record_phase['label'])
                        for record_phase in record['order_phase_list']]
    order.order_phase_list.extend(order_phase_list)
    return order


ORDER_LIST.sort(key=lambda record: record['uid'])
ORDER_LIST = map(make_order, ORDER_LIST)

if DEBUG:
    map(pprint, ORDER_LIST)
