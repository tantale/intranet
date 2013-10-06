"""
:module: intranet.websetup.order_list
:date: 2013-10-06
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.model.pointage.order import Order
from intranet.model.pointage.order_phase import OrderPhase
import datetime
import json
import pkg_resources


def parse_date(date_str):
    if date_str:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        return None


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


def get_order_list():
    package = 'intranet.websetup'
    filename = 'order_list.json'
    json_path = pkg_resources.resource_filename(package, filename)  # @UndefinedVariable  @IgnorePep8
    with file(json_path, 'rb') as json_file:
        record_list = json.load(json_file)
    return map(make_order, record_list)
