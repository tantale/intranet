# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.order.get_all
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
%if order_list:
<div id="accordion">
%for order in order_list:
<h2 id="order_${order.uid}" class="searchable ${order.project_cat}">${order.order_ref}</h2>
<div>
%if order.order_phase_list:
<ul class="sortable">
%for order_phase in order.order_phase_list:
<li id="order_phase_${order_phase.uid}" class="ui-state-default">\
<span class="ui-icon ui-icon-arrowthick-2-n-s"></span>\
<span class="editInPlace">${order_phase.label}</span></li>
%endfor
</ul>
%else:
<p>Aucune phase</p>
%endif
<p class="alignCenter">
<a class="addButton" href="#">Ajouter une phase</a>
</p>
</div>
%endfor
</div>
<script type='text/javascript'>
    $('#accordion .minimal_form').ajaxForm({
        target : '#employee_content'
    });
    $('#accordion form button').button();
    $("#accordion").accordion({
        autoHeight : false,
        heightStyle : "fill",
        clearStyle: true
    });
</script>
%else:
<p>Aucune commande</p>
%endif
