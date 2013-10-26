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
<% div_phases_id = 'order_phase_frame_{}'.format(order.uid) %>
<h2 id="order_${order.uid}" class="searchable"><a
	href="../order_phase/?order_uid=${order.uid}">${order.order_ref}</a></h2>
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
	function load_order_content(header) {
		var uid = header.attr('id').split('_')[1];
		var url = './' + uid + '/edit';
		console.log('Load order content from URL: ' + url);
		$('#order_content').load(url);
		$('#order_get_all input[name=uid]').val(uid);
		$('#order_get_all input[name=order_ref]').val("");
	}
	$('#accordion .minimal_form').ajaxForm({
		target : '#order_content',
		beforeSubmit: function(arr, $form, options) {
			$('#flash').hide();
		}
	});
	$('#accordion form button').button();
	$('#accordion').click(function(){
		$('#accordion .ui-icon.ui-icon-arrowthick-2-n-s').hide();
	});
	$('#accordion').accordion({
		active: ${active_index_json|n},
		collapsible: true,
		heightStyle: "content",
		beforeActivate: function(event, ui) {
			if (ui.newHeader.attr('id')) {
				load_phase_list(ui.newHeader);
			} else if (ui.oldHeader.attr('id')) {
				console.log("empty #order_content...");
				$('#order_content').empty();
			}
		},
		activate: function(event, ui) {
			$('#accordion').accordion("refresh");
			if (ui.newHeader.attr('id')) {
				load_order_content(ui.newHeader);
				$('#accordion .ui-icon.ui-icon-arrowthick-2-n-s').show();
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
