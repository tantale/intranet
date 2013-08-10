# -*- coding: utf-8 -*-
"""Setup the Intranet-1.0 application"""
from intranet import model
from sqlalchemy.exc import IntegrityError
import collections
import logging
import transaction
#from tg import config

LOG = logging.getLogger(__name__)


def bootstrap(command, conf, vars):  # @ReservedAssignment
    """Place any commands to setup intranet here"""
    # -- initialize the order categories
    try:
        cat_dict = collections.OrderedDict()
        cat_dict.update({u"Commandes client":
                         [dict(cat_name=u"colorCuisines",
                               label=u"Cuisines",
                               css_def=u"background-color: yellow; color: black;"),
                          dict(cat_name=u"colorBains",
                               label=u"Bains",
                               css_def=u"background-color: #64FE2E; color: black;"),
                          dict(cat_name=u"colorBureaux",
                               label=u"Bureaux",
                               css_def=u"background-color: orange; color: black;"),
                          dict(cat_name=u"colorDressings",
                               label=u"Dressings",
                               css_def=u"background-color: aqua; color: black;"),
                          dict(cat_name=u"colorMagasins",
                               label=u"Magasins",
                               css_def=u"background-color: pink; color: black;"),
                          dict(cat_name=u"colorMeubles",
                               label=u"Meubles",
                               css_def=u"background-color: red; color: black;")]})
        cat_dict.update({u"Projets interne":
                         [dict(cat_name=u"colorRenovation",
                               label=u"Rénovation",
                               css_def=u"background-color: #0B610B; color: white;")]})
        cat_dict.update({u"Hors projet":
                         [dict(cat_name=u"colorConges",
                                label=u"Congés",
                                css_def=u"background-color: #6A0888; color: white;"),
                           dict(cat_name=u"colorNettoyage",
                                label=u"Nettoyage",
                                css_def=u"background-color: #61380B; color: white;"),
                           dict(cat_name=u"colorDechargement",
                                label=u"Déchargement",
                                css_def=u"background-color: #8A2908; color: white;")]})
        for group, entry_list in cat_dict.iteritems():
            LOG.info(u"Add order category's group: {}".format(group))
            for entry in entry_list:
                LOG.info(u"- Add order category: {}".format(entry['cat_name']))
                order_cat = model.OrderCat(cat_group=group, **entry)
                model.DBSession.add(order_cat)
            transaction.commit()
    except IntegrityError:
        print ('There was a problem adding your order categories data, '
               'they may have already been added:')
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'
