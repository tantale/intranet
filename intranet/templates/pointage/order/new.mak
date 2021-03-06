# -*- coding: utf-8 -*-
<div>
<!--<%doc>
:template: intranet.templates.pointage.order.new
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
-->
%if flash:
	${flash | n}
%endif
<form id="order_create" class="ui-widget"
	action="${tg.url('./')}"
	method="post" enctype="multipart/form-data">
	<fieldset>
		<legend class="ui-widget-header">Saisir les informations concernant une nouvelle commande</legend>
		<table>
			<tr>
				<td><p><label for="order_create__order_ref">Ref. commande :</label>
						<input id="order_create__order_ref" type="text" name="order_ref"
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
				<td><p><label for="order_create__project_cat">Catégorie :</label>
					<!--<%
						project_cat_list = [cat for cat_list in cat_dict.itervalues()
											for cat in cat_list]
						default_cat = project_cat_list[0].cat_name if project_cat_list else None
						curr_project_cat = values.get('project_cat', default_cat)
						found_list = filter(lambda cat: cat.cat_name == curr_project_cat, project_cat_list)
					%>-->
						<select id="order_create__project_cat" name="project_cat"
							class="${curr_project_cat}"
							title="Catégorie de projet">
                            %if cat_dict:
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
                                %if not found_list:
                                <optgroup label="${_(u'Sans catégorie')}" class="noColor">
                                    <option selected="selected"
                                        class="${curr_project_cat}"
                                        value="${curr_project_cat}">${curr_project_cat[5:]}</option>
                                </optgroup>
                                %endif
                            %else:
                                <!-- not cat_dict ==> use missing_order_cat_label -->
                                <option selected="selected">${missing_order_cat_label}</option>
                            %endif
						</select>
					%if 'project_cat' in form_errors:
					<span class="error">${form_errors['project_cat']}</span>
					%endif
					</p>
				</td>
			</tr>
			<tr>
				<td><p><label for="order_create__creation_date">Date de création :</label>
						<input id="order_create__creation_date" type="date" name="creation_date"
							value="${values.get('creation_date')}"
							title="Date de création de la commande (requise)" />
					%if 'creation_date' in form_errors:
					<span class="error">${form_errors['creation_date']}</span>
					%endif
					</p>
				</td>
			</tr>
			<tr>
				<td><p><label for="order_create__close_date">Date de clôture :</label>
						<input id="order_create__close_date" type="date" name="close_date"
							value="${values.get('close_date')}"
							title="Date de clôture de la commande (optionnelle)" />
					%if 'close_date' in form_errors:
					<span class="error">${form_errors['close_date']}</span>
					%endif
					</p>
				</td>
			</tr>
			<tr>
				<td class="alignRight">
				<button id="order_create__create" type="submit" class="create_button"
					title="Saisir les informations concernant une nouvelle commande">Créer</button></td>
			</tr>
		</table>
	</fieldset>
</form>
<script type='text/javascript'><!--
	"use strict";
	/*global $*/
	var project_cat_css = $('#order_create__project_cat').val();
	$('#order_create__project_cat').change(function(){
		var new_css = $(this).find('option:selected').attr('class');
		$(this).removeClass(project_cat_css).addClass(new_css);
		project_cat_css = new_css;
	});
	$('#order_content .create_button').button({
		text : true,
		icons : {
			primary : "ui-icon-check"
		}
	});
	$('#order_create').ajaxForm({
		target : '#order_content',
		beforeSubmit: function(arr, form, options) {
			$('#flash').hide();
		},
		success: function(responseJson, statusText, xhr) {
			// {"action": "post", "result": "ok", "values": {"order_ref": "Copie de DUJARDIN - Bain (3)"}}
			console.dir(responseJson);
			if (responseJson.result === "ok") {
				var order = responseJson.values, //
					order_get_all = $('#order_get_all');
				order_get_all.find('input[name=uid]').val("");
				order_get_all.find('input[name=order_ref]').val(order.order_ref);
				order_get_all.submit();
			} else {
				console.log("ERROR: don't update the order list.");
			}
		}
	});
--></script>
</div>