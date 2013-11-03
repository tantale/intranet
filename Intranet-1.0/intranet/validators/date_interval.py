# -*- coding: utf-8 -*-
"""
:module: intranet.validators.date_interval
:date: 2013-11-03
:author: Laurent LAPORTE <sandlol2009@gmail.com>
"""


def check_date_interval(start_date, end_date):
    if end_date is None or start_date < end_date:
        return dict(status="ok")
    elif start_date == end_date:
        msg_fmt = (u"L'intervalle de dates n'est pas valide, "
                   u"dates identiques : "
                   u"{start_date:%d/%m/%Y} = {end_date:%d/%m/%Y}.")
        err_msg = msg_fmt.format(start_date=start_date,
                                 end_date=end_date)
        return dict(message=err_msg, status="error")
    else:
        msg_fmt = (u"L'intervalle de dates n'est pas valide, "
                   u"ordre des dates inversé : "
                   u"{start_date:%d/%m/%Y} > {end_date:%d/%m/%Y}.")
        err_msg = msg_fmt.format(start_date=start_date,
                                 end_date=end_date)
        return dict(message=err_msg, status="error")
