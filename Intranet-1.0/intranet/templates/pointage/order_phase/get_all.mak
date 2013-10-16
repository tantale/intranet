# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.order_phase.get_all
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%
div_phases_id = 'order_phase_frame_{}'.format(order_uid)
div_content_id = 'order_phase_content_{}'.format(order_uid)
ul_list_id = 'order_phase_list_{}'.format(order_uid)
p_empty_id = 'order_phase_list_empty_{}'.format(order_uid)
div_bottom_id = 'order_phase_bottom_{}'.format(order_uid)
form_post_id = 'order_phase_post_{}'.format(order_uid)
%>
<div id="${div_content_id}" class="order_phase_content ${project_cat}">
%if order_phase_list:
	%if editable:
	<ul id="${ul_list_id}" class="order_phase_list sortable">
	%for order_phase in order_phase_list:
		<li id="order_phase_li_${order_phase.uid}"
			class="ui-state-default"><span
			class="ui-icon ui-icon-arrowthick-2-n-s"></span><span
			id="order_phase_label_${order_phase.uid}"
			class="order_phase editable">${order_phase.label}</span></li>
	%endfor
	</ul>
	%elif selectable:
	<ul id="${ul_list_id}" class="order_phase_list selectable">
	%for order_phase in order_phase_list:
		<li id="order_phase_li_${order_phase.uid}"
			class="ui-widget-content"><span
			id="order_phase_label_${order_phase.uid}"
			class="order_phase">${order_phase.label}</span></li>
	%endfor
	</ul>
	%endif
%else:
	<p id="${p_empty_id}"
	class="empty_order_phase_list alignCenter"><em>Aucune phase</em></p>
%endif
%if editable:
<div id="${div_bottom_id}" class="order_phase_bottom">
<form id="${form_post_id}" class="inline_form alignCenter"
	action="${tg.url('../order_phase/')}"
	method="post">
	<p><input type="hidden" name="order_uid" value="${order_uid}"
		/><input id="${form_post_id}__label" type="text" name="label"
		value="" placeholder="Libellé"
		title="Libellé de la phase (requis)" />
		<button id="${form_post_id}__post" type="submit" class="post_button"
					title="Ajoute une nouvelle phase">Ajouter</button></p>
</form>
</div>
%endif
</div>
<script type='text/javascript'>
	"use strict";
	%if editable:
	$('#${ul_list_id}').sortable({
		update: function(event, ui) {
			var child_list = ui.item.parent().children(), uid_list = [], data;
			$.each(child_list, function(index, item) {
				uid_list[index] = $(item).attr('id').split('_')[3];
			});
			data = {uids: uid_list.join('|'), delim: '|'};
			$.post("${tg.url('../order_phase/reorder')}", data);
		}
	});
	$('#${ul_list_id}').disableSelection();
	$('#${ul_list_id} .editable').editable({
		type: "text",
		pk: "unused",
		url: "${tg.url('../order_phase/edit_in_place')}",
		title: "Saisir le libellé de la phase",
		placeholder: "Libellé",
		emptytext: "Vide",
		clear: true,
		showbuttons: false,
		onblur: "cancel",
		success: function(response, newValue) {
			if (response.status === 'error') {
				// assume server response: 200 Ok {status: 'error', msg: 'field cannot be empty!'}
				// msg will be shown in editable form
				return response.msg;
			} else if (response.status === 'deleted') {
				$(this).editable('option', 'emptytext', response.label);
				var div_phases = $('#${div_phases_id}'),
					header = div_phases.prev();
				var url = header.children('a').attr('href');
				console.log('Load phases list from URL: ' + url);
				div_phases.load(url);
			}
		}
	});
	%elif selectable:
	$("#${ul_list_id} li")
	.zIndex(1000)
	.draggable({
		appendTo: 'body',
		containment: false,
		cursor: 'move',
		cursorAt: {left: 5},
		delay: 300,
		distance: 10,
		// helper: 'clone',
		helper: function() {
			var li = $('<li class="ui-widget-content drag-selected"></li>').text($(this).text());
			return $('<ul class="selectable"></ul>').append(li)[0];
		},
		opacity: 0.9,
		revert: 'invalid',
		revertDuration: 300,
		scroll: true,
		start: function() {
			$(this).trigger('click');
		}
	})
	.removeClass('ui-selecting ui-selected')
	.mouseenter(function() {
		if ($(this).hasClass('ui-selected')) {
		} else {
			$(this).addClass('ui-selecting');
		}
	})
	.mouseleave(function() {
		if ($(this).hasClass('ui-selected')) {
		} else {
			$(this).removeClass('ui-selecting');
		}
	})
	.click(function() {
		$('ul.selectable li').removeClass('ui-selecting ui-selected');
		$(this).addClass('ui-selected');
	});
	%endif
	$('#${form_post_id} .post_button').button({
		text: false,
		icons: {
			primary: "ui-icon-plus"
		}
	});
	$('#${form_post_id} input[name=label]').focus();
	$('#${form_post_id}').ajaxForm({
		target : '#${div_phases_id}'
	});
</script>
