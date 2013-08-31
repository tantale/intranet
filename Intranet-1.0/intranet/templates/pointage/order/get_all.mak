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
<% div_frame_id = 'order_phase_frame_{}'.format(order.uid) %>
<h2 id="order_${order.uid}" class="searchable"><a
	href="/pointage/order_phase/?order_uid=${order.uid}">${order.order_ref}</a></h2>
<div id="${div_frame_id}"><em class="loading">Chargement en cours...</em></div>
%endfor
</div>
<% active_index_json = json.dumps(active_index) %>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	function load_phase_list(header) {
		var phases_div = header.next();
		if (phases_div.find('em.loading').length != 0) {
			var url = header.children('a').attr('href');
			console.log('load phase list from url: ' + url);
			phases_div.load(url);
		} else {
			console.log('phase list already loaded.');
		}
	}
	function load_order_content(header) {
		var uid = header.attr('id').split('_')[1];
		var url = '/pointage/order/' + uid + '/edit';
		console.log('load order content from url: ' + url);
		$('#order_content').load(url);
		$("#order_get_all input[name=uid]").val(uid);
	}
	$('#accordion .minimal_form').ajaxForm({
		target : '#order_content'
	});
	$('#accordion form button').button();
	$("#accordion").accordion({
		active: ${active_index_json|n},
		collapsible: true,
		heightStyle: "content",
		beforeActivate: function(event, ui) {
			if (ui.newHeader.attr('id')) {
				load_phase_list(ui.newHeader);
			}
		},
		activate: function(event, ui) {
			$("#accordion").accordion("refresh");
			if (ui.newHeader.attr('id')) {
				load_order_content(ui.newHeader);
			} else if (ui.oldHeader.attr('id')) {
				$('#order_content').empty();
			}
		},
		create: function(event, ui) {
			if (ui.header.attr('id')) {
				load_phase_list(ui.header);
				load_order_content(ui.header);
			}
		}
	});
</script>
%else:
<p>Aucune commande</p>
%endif
