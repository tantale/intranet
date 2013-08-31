# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.order_phase.get_all
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%
div_frame_id = 'order_phase_frame_{}'.format(order_uid)
div_content_id = 'order_phase_content_{}'.format(order_uid)
ul_list_id = 'order_phase_list_{}'.format(order_uid)
p_empty_id = 'order_phase_list_empty_{}'.format(order_uid)
div_bottom_id = 'order_phase_bottom_{}'.format(order_uid)
form_post_id = 'order_phase_post_{}'.format(order_uid)
%>
<div id="${div_content_id}" class="order_phase_content ${project_cat}">
%if order_phase_list:
<ul id="${ul_list_id}" class="order_phase_list sortable">
%for order_phase in order_phase_list:
    <li class="ui-state-default"><span
        class="ui-icon ui-icon-arrowthick-2-n-s"></span><span
        id="order_phase_${order_phase.uid}"
        class="order_phase editable">${order_phase.label}</span></li>
%endfor
</ul>
%else:
    <p id="${p_empty_id}"
    class="empty_order_phase_list alignCenter"><em>Aucune phase</em></p>
%endif
<div id="${div_bottom_id}" class="order_phase_bottom">
<form id="${form_post_id}" class="inline_form alignCenter"
    action="${tg.url('/pointage/order_phase/')}"
    method="post">
    <p><input type="hidden" name="order_uid" value="${order_uid}"
    	/><input id="${form_post_id}__label" type="text" name="label"
        value="" placeholder="Libellé"
        title="Libellé de la phase (requis)" />
        <button id="${form_post_id}__post" type="submit" class="post_button"
                    title="Ajoute une nouvelle phase">Ajouter</button></p>
</form>
</div>
</div>
<script type='text/javascript'>
    "use strict";
	$("#${ul_list_id}").sortable();
	$("#${ul_list_id}").disableSelection();
	$("#${ul_list_id} .editable").editInPlace({
		url : "http://com.examplesite.www/users",
		params : "name=david"
	});
    $("#${form_post_id} .post_button").button({
        text: false,
        icons: {
            primary: "ui-icon-plus"
        }
    });
	$('#${form_post_id}').ajaxForm({
		target : '#${div_frame_id}'
	});
</script>
