# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.order.edit
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%! import json %>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if flash:
	${flash | n}
%endif
<form id="order_update" class="ui-widget"
	action="${tg.url('/pointage/order/{uid}'.format(uid=values['uid']))}"
	method="post" enctype="multipart/form-data">
	<fieldset>
		<legend class="ui-widget-header">Modifier les informations concernant la commande ${values.get('order_ref')}</legend>
		<table>
			<tr>
				<td><p><label for="order_update__order_ref">Ref. commande :</label>
						<input id="order_update__order_ref" type="text" name="order_ref"
							value="${values.get('order_ref')}"
							placeholder="Référence"
							title="Référence de la commande (requis)" />
					%if 'order_ref' in form_errors:
					<span class="error">${form_errors['order_ref']}</span>
					%endif
					</p>
				</td>
			</tr>
			<tr>
				<td><p><label for="order_update__project_cat">Catégorie :</label>
					<%
						project_cat_list = [cat for cat_list in cat_dict.itervalues()
											for cat in cat_list]
						default_cat = project_cat_list[0].cat_name if project_cat_list else None
						curr_project_cat = values.get('project_cat', default_cat)
					%>
						<select id="order_update__project_cat" name="project_cat"
							class="${curr_project_cat}"
							title="Catégorie de projet">
							%for cat_group, order_cat_list in cat_dict.iteritems():
							<optgroup label="${cat_group}" class="noColor">
								%for order_cat in order_cat_list:
								%if order_cat.cat_name == curr_project_cat:
								<option selected="selected"
									class="${order_cat.cat_name}"
									value="${order_cat.cat_name}">${order_cat.label}</option>
								%else:
								<option
									class="${order_cat.cat_name}"
									value="${order_cat.cat_name}">${order_cat.label}</option>
								%endif
								%endfor
							</optgroup>
							%endfor
						</select>
					%if 'project_cat' in form_errors:
					<span class="error">${form_errors['project_cat']}</span>
					%endif
					</p>
				</td>
			</tr>
			<tr>
				<td><p><label for="order_update__creation_date">Date de création :</label>
						<input id="order_update__creation_date" type="date" name="creation_date"
							value="${values.get('creation_date')}"
							title="Date de création de la commande (requis)" />
					%if 'creation_date' in form_errors:
					<span class="error">${form_errors['creation_date']}</span>
					%endif
					</p>
				</td>
			</tr>
			<tr>
				<td><p><label for="order_update__close_date">Date de clôture :</label>
						<input id="order_update__close_date" type="date" name="close_date"
							value="${values.get('close_date')}"
							title="Date de clôture de la commande (optionnel)" />
					%if 'close_date' in form_errors:
					<span class="error">${form_errors['close_date']}</span>
					%endif
					</p>
				</td>
			</tr>
			<tr>
				<td class="alignRight">
				<input type="hidden" name="_method" value="PUT" />
				<button id="order_update__update" type="submit" class="update_button"
					title="Modifier les informations concernant la commande">Modifier</button></td>
			</tr>
		</table>
	</fieldset>
</form>

<form id="order_get_delete" class="minimal_form"
	action="${tg.url('/pointage/order/{uid}/delete'.format(uid=values['uid']))}"
	method="get">
	<p>
		<button id="order_get_delete__delete" type="submit" class="delete_button"
			title="Supprimer les informations concernant la commande ${values.get('order_ref')}">Supprimer</button>
	</p>
</form>

<script type='text/javascript'>
	"use strict";
	/*global $, Modernizr*/
	var project_cat_css = $('#order_update__project_cat').val();
	$('#order_update__project_cat').change(function(){
		var new_css = $(this).find('option:selected').attr('class');
		$(this).removeClass(project_cat_css).addClass(new_css);
		project_cat_css = new_css;
	});
	if (!Modernizr.inputtypes.date) {
		$('#order_content input[type=date]').datepicker();
	}
	$("#order_content .update_button").button({
		text : true,
		icons : {
			primary : "ui-icon-check"
		}
	});
	$('#order_update').ajaxForm({
		target : '#order_content',
		success: function(responseText, statusText, xhr) {
			console.log("search for '<div id=\"flash\"><div class=\"ok\">' tag...");
			var ok = $('<div/>').append(responseText).find('#flash div.ok');
			if (ok.length) {
				var input = $("#order_get_all input[name=uid]"),
					uid = input.val();
				console.log("OK, update the order list but don't select any order...");
				input.val("");
				$("#order_get_all").submit();
				input.val(uid);
			} else {
				console.log("ERROR: don't update the order list.");
			}
		}
	});
	$("#order_get_delete .delete_button").button({
		text : true,
		icons : {
			primary : "ui-icon-trash"
		}
	});
	$('#order_get_delete').ajaxForm({
		target : '#confirm_dialog_content'
	});
</script>
