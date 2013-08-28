# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.order.get_all
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%! import json %>
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
<% active_index_json = json.dumps(active_index) %>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$('#accordion .minimal_form').ajaxForm({
		target : '#order_content'
	});
	$('#accordion form button').button();
	$("#accordion").accordion({
		active: ${active_index_json|n},
		collapsible: true,
		heightStyle: "auto",
		activate: function(event, ui) {
			if (ui.newHeader.attr('id')) {
				var uid = ui.newHeader.attr('id').split('_')[1],
					url = '/pointage/order/' + uid + '/edit';
				$('#order_content').load(url);
				$("#order_get_all input[name=uid]").val(uid);
			} else if (ui.oldHeader.attr('id')) {
				$('#order_content').text("");
			}
		},
		create: function(event, ui) {
			if (ui.header.attr('id')) {
				var uid = ui.header.attr('id').split('_')[1],
					url = '/pointage/order/' + uid + '/edit';
				$('#order_content').load(url);
				$("#order_get_all input[name=uid]").val(uid);
			} else if (ui.oldHeader.attr('id')) {
				$('#order_content').text("");
			}
		}
	});
</script>
%else:
<p>Aucune commande</p>
%endif
