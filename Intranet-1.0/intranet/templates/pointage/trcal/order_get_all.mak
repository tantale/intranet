# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.trcal.order_get_all
:date: 2013-09-22
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%! import json %>
%if order_list:
<div id="accordion">
%for order in order_list:
<% div_phases_id = 'order_phase_frame_{}'.format(order.uid) %>
<h2 id="order_${order.uid}" class="searchable"><a
    href="../order_phase/?order_uid=${order.uid}&editable=False&selectable=True">${order.order_ref}</a></h2>
<div id="${div_phases_id}"><em class="loading">Chargement en cours...</em></div>
%endfor
</div>
<% active_index_json = json.dumps(active_index) %>
<script type='text/javascript'>
    "use strict";
    /*global $*/
    function load_phase_list(header) {
        var div_phases = header.next();
        if (div_phases.find('em.loading').length != 0) {
            var url = header.children('a').attr('href');
            console.log('Load phases list from URL: ' + url);
            div_phases.load(url);
        } else {
            console.log('Phases list is already loaded.');
        }
    }

    function scroll_phase_list(header) {
        var scrollable = header.offsetParent(), //
            scrollable_offset = scrollable.offset(), //
            offset = header.offset();
        scrollable.scrollTop(offset.top - scrollable_offset.top);
    }

    $('#accordion form button').button();
    $('#accordion').accordion({
        active: ${active_index_json|n},
        collapsible: true,
        heightStyle: "content",
        beforeActivate: function(event, ui) {
            if (ui.newHeader.attr('id')) {
                load_phase_list(ui.newHeader);
            } else if (ui.oldHeader.attr('id')) {
            }
        },
        activate: function(event, ui) {
            $('#accordion').accordion("refresh");
            if (ui.newHeader.attr('id')) {
            }
        },
        create: function(event, ui) {
            if (ui.header.attr('id')) {
                scroll_phase_list(ui.header);
                load_phase_list(ui.header);
            }
        }
    });
</script>
%else:
<p>Aucune commande</p>
%endif
