# -*- coding: utf-8 -*-
"""WebHelpers used in Intranet-1.0."""
import datetime
from webhelpers import date, feedgenerator, html, number, misc, text


def current_year():
    now = datetime.datetime.now()
    return now.strftime('%Y')


def icon(icon_name, white=False):
    if (white):
        return html.literal('<i class="icon-%s icon-white"></i>' % icon_name)
    else:
        return html.literal('<i class="icon-%s"></i>' % icon_name)
