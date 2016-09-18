# -*- coding: utf-8 -*-
from sqlalchemy import and_
from sqlalchemy import or_


# noinspection PyComparisonWithNone
def overlap_cond(ref_start, ref_end, field_start, field_end):
    """
    Construct a sqlalchemy's predicate to check if two date intervals overlap.

    :param ref_start: reference interval start date

    :param ref_end: reference interval end date

    :param field_start: field interval start date

    :param field_end: field interval end date, or None for eternity

    :return: ref_start <= field_start < ref_end or
             field_start <= ref_start < field_end
    """
    return or_(and_(field_start >= ref_start,
                    field_start < ref_end),
               and_(field_start <= ref_start,
                    or_(field_end == None, field_end > ref_start)))
