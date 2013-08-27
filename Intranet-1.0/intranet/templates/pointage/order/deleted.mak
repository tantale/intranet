# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.order.deleted
:date: 2013-08-19
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if flash:
    ${flash | n}
%endif
