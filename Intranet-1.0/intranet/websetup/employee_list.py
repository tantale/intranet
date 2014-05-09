"""
:module: intranet.websetup.employee_list
:date: 2013-10-05
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
from intranet.model.pointage.employee import Employee
import datetime
import json
import pkg_resources


def parse_date(date_str):
    if date_str:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        return None


def make_employee(record):
    return Employee(employee_name=record['employee_name'],
                    worked_hours=float(record['worked_hours']),
                    entry_date=parse_date(record['entry_date']),
                    exit_date=parse_date(record['exit_date']),
                    photo_path=record['photo_path'])


def get_employee_list():
    package = 'intranet.websetup'
    filename = 'employee_list.json'
    json_path = pkg_resources.resource_filename(package, filename)  # @UndefinedVariable  @IgnorePep8
    with file(json_path, 'rb') as json_file:
        record_list = json.load(json_file)
    return map(make_employee, record_list)
