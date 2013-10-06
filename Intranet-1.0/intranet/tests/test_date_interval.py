"""
:module: intranet.tests.test_date_interval
:date: 2013-09-21
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""
import datetime
import unittest


def create_date_range_list():
    start_before = datetime.date(2013, 4, 10)
    start_inside = datetime.date(2013, 5, 10)
    start_after = datetime.date(2013, 6, 10)

    end_before = datetime.date(2013, 4, 20)
    end_inside = datetime.date(2013, 5, 20)
    end_after = datetime.date(2013, 6, 20)

    range_list = []
    for start_date in (start_before, start_inside, start_after):
        for end_date in (end_before, end_inside, end_after):
            if start_date <= end_date:
                range_list.append((start_date, end_date))
    return range_list


def overlap1(r1, r2):
    latest_start = max(r1[0], r2[0])
    earliest_end = min(r1[1], r2[1])
    overlap = earliest_end - latest_start
    return overlap.days >= 0


def overlap2(r1, r2):
    return (r1[0] <= r2[0] <= r1[1]) or (r2[0] <= r1[0] <= r2[1])


def overlap3(r1, r2):
    field_start, field_end = r1
    ref_start, ref_end = r2
    return ((field_start >= ref_start and field_start < ref_end) or
            (field_start <= ref_start and (field_end == None or
                                           field_end > ref_start)))


employee_list = [{'employee_name': 'e1',
                  'entry_date': '2013-08-10',
                  'exit_date': '2013-08-20',
                  'photo_path': None,
                  'uid': 1,
                  'worked_hours': 39},
                 {'employee_name': 'e2',
                  'entry_date': '2013-08-10',
                  'exit_date': '2013-09-20',
                  'photo_path': None,
                  'uid': 2,
                  'worked_hours': 39},
                 {'employee_name': 'e3',
                  'entry_date': '2013-08-10',
                  'exit_date': '2013-10-20',
                  'photo_path': None,
                  'uid': 3,
                  'worked_hours': 39},
                 {'employee_name': 'e4',
                  'entry_date': '2013-09-10',
                  'exit_date': '2013-09-20',
                  'photo_path': None,
                  'uid': 4,
                  'worked_hours': 39},
                 {'employee_name': 'e5',
                  'entry_date': '2013-09-10',
                  'exit_date': '2013-10-20',
                  'photo_path': None,
                  'uid': 5,
                  'worked_hours': 39},
                 {'employee_name': 'e6',
                  'entry_date': '2013-10-10',
                  'exit_date': '2013-10-20',
                  'photo_path': None,
                  'uid': 6,
                  'worked_hours': 39},
                 {'employee_name': 'e7',
                  'entry_date': '2013-08-10',
                  'exit_date': None,
                  'photo_path': None,
                  'uid': 7,
                  'worked_hours': 39},
                 {'employee_name': 'e8',
                  'entry_date': '2013-09-10',
                  'exit_date': None,
                  'photo_path': None,
                  'uid': 8,
                  'worked_hours': 39},
                 {'employee_name': 'e9',
                  'entry_date': '2013-10-10',
                  'exit_date': None,
                  'photo_path': None,
                  'uid': 9,
                  'worked_hours': 39}]


class TestDateIntervals(unittest.TestCase):
    """
    """

    def test_overlap(self):
        fmt = "from {start} to {end}"
        curr_range = (datetime.date(2013, 5, 1),
                      datetime.date(2013, 5, 31))
        print(fmt.format(start=curr_range[0], end=curr_range[1]))
        date_range_list = create_date_range_list()
        for date_range in date_range_list:
            result1 = overlap1(date_range, curr_range)
            result2 = overlap2(date_range, curr_range)
            range_ = fmt.format(start=date_range[0], end=date_range[1])
            print("Date {range} overlap?: {result1},  {result2}"
                  .format(range=range_,
                          result1=result1,
                          result2=result2))

    def test_employee_list(self):
        curr_range = (datetime.date(2013, 9, 1),
                      datetime.date(2013, 10, 1))

        for employee in employee_list:
            start = datetime.datetime.strptime(employee['entry_date'],
                                               '%Y-%m-%d').date()
            if employee['exit_date']:
                end = datetime.datetime.strptime(employee['exit_date'],
                                                 '%Y-%m-%d').date()
            else:
                end = None
            date_range = (start, end)
            print date_range, curr_range, overlap3(date_range, curr_range)


if __name__ == "__main__":
    unittest.main()
