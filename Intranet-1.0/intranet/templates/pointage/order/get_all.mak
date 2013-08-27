# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.order.get_all
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
%if order_list:
<div id="accordion">
%for order in order_list:
<h2 id="order_${order.uid}" class="searchable">${order.order_ref}</h2>
<div>
%if order.order_phase_list:
<ul class="sortable ${order.project_cat}">
%for order_phase in order.order_phase_list:
<li id="order_phase_${order_phase.uid}" class="ui-state-default">\
<span class="ui-icon ui-icon-arrowthick-2-n-s"></span>\
<span class="editInPlace">${order_phase.label}</span></li>
%endfor
</ul>
%else:
<p class="${order.project_cat}">Aucune phase</p>
%endif
<p class="alignCenter">
<a class="addButton" href="#">Ajouter une phase</a>
</p>
</div>
%endfor
</div>
<script type='text/javascript'>
    "use strict";
    /*global $*/
    $('#accordion .minimal_form').ajaxForm({
        target : '#order_content'
    });
    $('#accordion form button').button();
    $("#accordion").accordion({
        active: ${active_index},
        collapsible: true,
        heightStyle: "auto",
        activate: function(event, ui) {
            var uid = ui.newHeader.attr('id').split('_')[1],
                url = '/pointage/order/' + uid + '/edit';
            $('#order_content').load(url);
            $("#order_get_all input[name=uid]").val(uid);
            $("#search_form input[name=uid]").val(uid);
        }
    });
</script>
%else:
<p>Aucune commande</p>
%endif
