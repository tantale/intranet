# -*- coding: utf-8 -*-
<div>
<!--<%!
import json
import datetime
%>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
-->
%if flash:
	${flash | n}
%endif
<style scoped="scoped">
    #order_update label {
        display: inline-block;
        text-align: left;
        font-weight: bold;
    }
    #order_update input.label             {font-weight: bold; width: 18em;}
    #order_update table.dates label       {width: 9em;}
    #order_update table.charge            {margin: 0 auto 0 auto;}
    #order_update table.charge th         {font-size: .8em;}
    #order_update table.charge input[type="number"] {text-align: right;}
</style>
<form id="order_update" class="ui-widget"
	action="${tg.url('./{uid}'.format(uid=values['uid']))}"
	method="post" enctype="multipart/form-data">
	<fieldset>
		<legend class="ui-widget-header">Modifier les informations concernant la commande ${values.get('order_ref')}</legend>
        ##
        ## Commande: uid + order_ref
        ##
        <div class="row-xs">
            <div class="col-xs-2">
                <label for="order_update__uid">Commande :</label>
            </div>
            <div class="col-xs-10">
                <input id="order_update__uid" type="number" name="uid"
                       value="${values['uid']}"
                       disabled="disabled"
                       style="width: 5em;"
                       title="Numéro de la commande (non modifiable)"/>
                <input id="order_update__order_ref" type="text" name="order_ref" class="label"
                       value="${values.get('order_ref')}"
                       style="width: 20em;"
                       placeholder="Référence"
                       title="Référence de la commande (requis)"/>
                %if 'order_ref' in form_errors:
                <p><span class="error">${form_errors['order_ref']}</span></p>
                %endif
            </div>
        </div>
        <div class="row-xs">
            <div class="col-xs-2">
                <label for="order_update__project_cat">Catégorie :</label>
            </div>
            <div class="col-xs-10">
                <%
                project_cat_list = [cat for cat_list in cat_dict.itervalues()
                for cat in cat_list]
                default_cat = project_cat_list[0].cat_name if project_cat_list else None
                curr_project_cat = values.get('project_cat', default_cat)
                found_list = filter(lambda cat: cat.cat_name == curr_project_cat, project_cat_list)
                %>
                <select id="order_update__project_cat" name="project_cat"
                        class="${curr_project_cat}"
                        title="Catégorie de projet">
                    %if cat_dict:
                    %for cat_group, order_cat_list in cat_dict.iteritems():
                    <optgroup label="${cat_group}" class="noColor">
                        %for order_cat in order_cat_list:
                        %if order_cat.cat_name == curr_project_cat:
                        <option selected="selected"
                                class="${order_cat.cat_name}"
                                value="${order_cat.cat_name}">${order_cat.label}
                        </option>
                        %else:
                        <option
                                class="${order_cat.cat_name}"
                                value="${order_cat.cat_name}">${order_cat.label}
                        </option>
                        %endif
                        %endfor
                    </optgroup>
                    %endfor
                    %if not found_list:
                    <optgroup label="${_(u'Sans catégorie')}" class="noColor">
                        <option selected="selected"
                                class="${curr_project_cat}"
                                value="${curr_project_cat}">${curr_project_cat[5:]}
                        </option>
                    </optgroup>
                    %endif
                    %else:
                    <!-- not cat_dict ==> use missing_order_cat_label -->
                    <option selected="selected">${missing_order_cat_label}</option>
                    %endif
                </select>
                %if 'project_cat' in form_errors:
                <p><span class="error">${form_errors['project_cat']}</span></p>
                %endif
            </div>
        </div>
        <div class="row-xs">
            <div class="col-xs-6">
                <table class="dates">
                    <tr>
                        <td><label for="order_update__creation_date">Date de création :</label>
                            <input id="order_update__creation_date" type="date" name="creation_date"
                                   value="${values.get('creation_date')}"
                                   title="Date de création de la commande (requise)"/>
                            %if 'creation_date' in form_errors:
                            <span class="error">${form_errors['creation_date']}</span>
                            %endif
                        </td>
                    </tr>
                    <tr>
                        <td><label for="order_update__close_date">Date de clôture :</label>
                            <input id="order_update__close_date" type="date" name="close_date"
                                   value="${values.get('close_date')}"
                                   title="Date de clôture de la commande (optionnelle)"/>
                            %if 'close_date' in form_errors:
                            <span class="error">${form_errors['close_date']}</span>
                            %endif
                        </td>
                    </tr>

                </table>
            </div>
            <div class="col-xs-6">
                <table class="charge">
                    <thead>
                    <tr>
                        <th></th>
                        <th>Estimée</th>
                        <th>Effectuée</th>
                        <th>Restante</th>
                        <th>Totale</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <th>Charge&nbsp;:</th>
                        <td>
                            <input class="change"
                                   name="estimated_duration" type="number" value="${order.estimated_duration}"
                                   readonly="readonly"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée estimée à partir des statistiques"/>
                        </td>
                        <td>
                            <input class="change"
                                   name="tracked_duration" type="number" value="${order.tracked_duration}"
                                   readonly="readonly"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée déjà effectuée et pointée"/>
                        </td>
                        <td>
                            <input class="change"
                                   name="remain_duration" type="number" value="${order.remain_duration}"
                                   readonly="readonly"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée restante estimée"/>
                        </td>
                        <td>
                            <input class="change"
                                   name="total_duration" type="number" value="${order.total_duration}"
                                   readonly="readonly"
                                   min="0" max="999" step=".25" placeholder="(heures)"
                                   title="Durée totale : effectuée + restante"/>
                        </td>
                    </tr>
                    <tr>
                        <th>Statut&nbsp;:</th>
                        <td colspan="4">
                            <div class="task_status">
                                %for status_info in order.all_status_info:
                                %if status_info['checked']:
                                <label title="${status_info['description']}"><input class="change"
                                                                                    disabled="disabled"
                                                                                    type="radio" checked="checked"
                                                                                    value="${status_info['value']}"
                                                                                    name="task_status"/>${status_info['label']}</label>
                                %else:
                                <label title="${status_info['description']}"><input class="change"
                                                                                    disabled="disabled"
                                                                                    type="radio"
                                                                                    value="${status_info['value']}"
                                                                                    name="task_status"/>${status_info['label']}</label>
                                %endif
                                %endfor
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="row-xs">
            <div class="col-xs-12">
                <nav>
                    <input type="hidden" name="_method" value="PUT"/>
                    <button id="order_update__update" type="submit" class="update_button"
                            title="Modifier les informations concernant la commande">Modifier
                    </button>
                    %if not values.get('close_date'):
                    <button id="order_update__close" type="submit" class="close_button"
                            title="Clôturer la commande à la date du jour">Clôturer
                    </button>
                    %endif
                </nav>
            </div>
        </div>
	</fieldset>
</form>

<div>
<form id="order_get_delete" class="inline_form"
	action="${tg.url('./{uid}/delete'.format(uid=values['uid']))}"
	method="get">
	<p>
		<button id="order_get_delete__delete" type="submit" class="delete_button"
			title="Supprimer les informations concernant la commande ${values.get('order_ref')}">Supprimer</button>
	</p>
</form>
<form id="order_duplicate" class="inline_form"
	action="${tg.url('./duplicate')}"
	method="get">
	<p>
		<input type="hidden" name="uid" value="${values['uid']}" />
		<button id="order_duplicate__copy" type="submit" class="copy_button"
			title="Créer une nouvelle commande en copiant les informations de ${values.get('order_ref')}">Dupliquer</button>
	</p>
</form>
<form id="order_chart_detail" class="inline_form"
	action="${tg.url('../chart/{uid}'.format(uid=values['uid']))}"
	method="get">
	<p>
		<button id="order_chart_detail__display" type="submit" class="display_button"
			title="Afficher les statistiques de pointage de la commande ${values.get('order_ref')}">Statistiques</button>
	</p>
</form>
<form id="order_estimate_all_form" class="inline_form"
	action="${tg.url('./{uid}/tasks/estimate_all_form'.format(uid=values['uid']))}"
	method="get">
	<p>
		<button id="order_estimate_all_form__display" type="submit" class="display_button"
			title="${_(u'Estimer les tâches de la commande {ref}').format(ref=values.get('order_ref'))}">${_(u"Estimer les tâches")}</button>
	</p>
</form>
</div>
<div id="order_tasks"></div>

<script type='text/javascript'><!--
	"use strict";
	/*global $*/
	var project_cat_css = $('#order_update__project_cat').val();
	$('#order_update__project_cat').change(function(){
		var new_css = $(this).find('option:selected').attr('class');
		$(this).removeClass(project_cat_css).addClass(new_css);
		project_cat_css = new_css;
	});
	$('#order_content .update_button').button({
		text : true,
		icons : {
			primary : "ui-icon-pencil"
		}
	});
%if not values.get('close_date'):
	$('#order_content .close_button').button({
		text : true,
		icons : {
			primary : "ui-icon-circle-close"
		}
	}).click(function(){
		var date = new Date();
		$('#order_update__close_date').val(date.toISOString().split("T")[0]);
	});
%endif
	$('#order_update').ajaxForm({
		target : '#order_content',
		beforeSubmit: function(arr, form, options) {
			$('#flash').hide();
		},
		success: function(responseText, statusText, xhr) {
			var ok = $('<div/>').append(responseText).find('#flash div.ok');
			if (ok.length) {
				var order_get_all = $('#order_get_all'), //
					input_uid = order_get_all.find('input[name=uid]'), //
					input_order_ref = order_get_all.find('input[name=order_ref]'),
					uid = input_uid.val();
				input_uid.val("");
				input_order_ref.val("");
				order_get_all.submit();
				input_uid.val(uid);
			}
		}
	});
	$('#order_get_delete .delete_button').button({
		text: true,
		icons: {
			primary : "ui-icon-trash"
		}
	});
	$('#order_get_delete').ajaxForm({
		target: '#confirm_dialog_content'
	});
	$('#order_duplicate .copy_button').button({
		text: true,
		icons: {
			primary : "ui-icon-copy"
		}
	});
	$('#order_duplicate').ajaxForm({
		target : '#order_content',
		beforeSubmit: function(arr, form, options) {
			$('#flash').hide();
		},
		success: function(responseJson, statusText, xhr) {
			// {"action": "duplicate", "result": "ok", "values": {"order_ref": "Copie de DUJARDIN - Bain (3)"}}
			if (responseJson.result === "ok") {
				var order = responseJson.values, //
					order_get_all = $('#order_get_all');
				order_get_all.find('input[name=uid]').val("");
				order_get_all.find('input[name=order_ref]').val(order.order_ref);
				order_get_all.submit();
			}
		}
	});
	$('#order_chart_detail .display_button').button({
		text: true,
		icons: {
			primary : "ui-icon-calculator"
		}
	});
	$('#order_chart_detail').ajaxForm({
		target: '#order_content'
	});
	$('#order_estimate_all_form .display_button').button({
		text: true,
		icons: {
			primary : "ui-icon-calendar"
		}
	});
%if values.get('close_date'):
    $('#order_estimate_all_form .display_button').button("disable");
%else:
    $('#order_estimate_all_form .display_button').button("enable");
%endif
	$('#order_estimate_all_form').ajaxForm({
		target: '#confirm_dialog_content',
		success: function(responseJson, statusText, xhr) {

			var thisDialog = $('#confirm_dialog').dialog({
				width: 500,
				height: 300,
				buttons: {
					"Estimer les tâches" : function() {
						$('#estimate_all_form').submit();
					},
					"Annuler": function() {
						$(this).dialog("close");
					}
				},
				title: "Estimer les tâches"
			});

			var ajaxFormProp = {
				beforeSubmit: function(arr, form, options) {
					$("body").css("cursor", "progress");
					return true;
				},
				error: function(responseText, statusText, xhr) {
					$("body").css("cursor", "default");
					$('#confirm_dialog_content').html('<p><span class="error">Échec de connexion au serveur</span></p>');
				},
				success: function(responseText, statusText, xhr) {
					$("body").css("cursor", "default");
					var error = $('<div/>').append(responseText).find('span.error');
					if (error.length) {
						$('#confirm_dialog_content').html(responseText);
						$('#estimate_all_form').ajaxForm(ajaxFormProp);
					} else {
						$('#order_tasks').html(responseText);
						thisDialog.dialog("close");
					}
				}
			};

			$('#estimate_all_form').ajaxForm(ajaxFormProp);

			thisDialog.dialog("open");
		}
	});
	var today = new Date();
	var tz_offset = today.getTimezoneOffset();
	var order_tasks_url = "${tg.url('./{uid}/tasks/'.format(uid=values['uid']))|n}" + "?&tz_offset=" + tz_offset;
	$('#order_tasks').load(order_tasks_url);
--></script>
</div>
