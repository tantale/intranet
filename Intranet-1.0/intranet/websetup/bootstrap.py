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
                         [dict(cat_name=u"colorMagasin",
                               label=u"Magasin",
                               css_def=u"background-color: #ea750c; color: white;"),  # @IgnorePep8
                          dict(cat_name=u"colorBureau",
                               label=u"Bureau",
                               css_def=u"background-color: #f6a9bc; color: black;"),  # @IgnorePep8
                          dict(cat_name=u"colorDressing",
                               label=u"Dressing",
                               css_def=u"background-color: #37ab51; color: white;"),  # @IgnorePep8
                          dict(cat_name=u"colorMeuble",
                               label=u"Meuble",
                               css_def=u"background-color: #bf0e1d; color: white;"),  # @IgnorePep8
                          dict(cat_name=u"colorMenuiserie",
                               label=u"Menuiserie",
                               css_def=u"background-color: #f7c181; color: black;"),  # @IgnorePep8
						  dict(cat_name=u"colorBain",
                               label=u"Salle de bain",
                               css_def=u"background-color: #009fe5; color: white;"),  # @IgnorePep8
                          dict(cat_name=u"colorCuisine",
                               label=u"Cuisine",
                               css_def=u"background-color: #fcc51c; color: black;")]})  # @IgnorePep8
        cat_dict.update({u"Projets interne":
                         [dict(cat_name=u"colorRenovation",
                               label=u"Rénovation",
                               css_def=u"background-color: #0B610B; color: white;")]})  # @IgnorePep8
        cat_dict.update({u"Hors projet":
                         [dict(cat_name=u"colorConges",
                                label=u"Congés",
                                css_def=u"background-color: #6A0888; color: white;"),  # @IgnorePep8
                           dict(cat_name=u"colorNettoyage",
                                label=u"Nettoyage",
                                css_def=u"background-color: #61380B; color: white;"),  # @IgnorePep8
                           dict(cat_name=u"colorDechargement",
                                label=u"Déchargement",
                                css_def=u"background-color: #8A2908; color: white;")]})  # @IgnorePep8
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
