<div>
    <!--
    <%! import collections %>
    <%flash = tg.flash_obj.render('flash', use_js=False)%>
    -->
    <div id="cat_groups">
        %if flash and not cat_group:
        ${flash | n}
        %endif
        %for label, order_cats in cat_group_index.iteritems():
        <!--<%
            first_uid = order_cats[0].uid
            cat_group_uid = "order_cat__cat_group__{0}".format(first_uid)
            cat_group_title = _(u"Cliquez sur le groupe \"{text}\" pour le modifier").format(text=label)
            create_form_uid = "order_cat_create_{0}".format(first_uid)
            create_form_title = _(u"Créer une nouvelle catégorie dans le groupe \"{text}\"").format(text=label)
        %>-->
        <h2><span id="${cat_group_uid}" class="cat_group editable" title="${cat_group_title}">${label}</span></h2>
        <table class="record-table" style="page-break-inside: avoid">
            <thead>
            <tr>
                <th class="record-table-name">${_(u"Code couleur")}</th>
                <th class="record-table-label">${_(u"Libellé")}</th>
                <th class="record-table-name">${_(u"Couleur du texte")}</th>
                <th class="record-table-name">${_(u"Couleur du fond")}</th>
                <th><!--empty--></th>
            </tr>
            </thead>
            <tbody>
            <!--
            %for order_cat in order_cats:
            <%
                fragid = "order_cat_{0}".format(order_cat.uid)
                delete_form_uid = "order_cat_get_delete_{0}".format(order_cat.uid)
                delete_form_title = _(u"Supprimer la catégorie \"{text}\"").format(text=order_cat.label)
                code_uid = "order_cat__code__{0}".format(order_cat.uid)
                label_uid    = "order_cat__label__{0}".format(order_cat.uid)
                fgcolor_uid  = "order_cat__fgcolor__{0}".format(order_cat.uid)
                bgcolor_uid  = "order_cat__bgcolor__{0}".format(order_cat.uid)
                code_title = _(u"Cliquez sur \"{text}\" pour le modifier").format(text=order_cat.code)
                label_title = _(u"Cliquez sur \"{text}\" pour le modifier").format(text=order_cat.label)
                fgcolor_title = _(u"Cliquez ici pour modifier la couleur du texte")
                bgcolor_title = _(u"Cliquez ici pour modifier la couleur du fond")
            %>
            -->
            <tr id="${fragid}" class="draggable droppable"
                title="${_(u'Glissez la catégorie {0} et déposez-la au-dessus d’un autre groupe pour lui attribuer ce groupe.').format(order_cat.label)}">
                <td class="record-table-name"><span id="${code_uid}" class="code editable"
                                                    title="${code_title}">${order_cat.code}</span></td>
                <td class="record-table-label">
                    <div
                            style="border: solid 1px black; padding: 4px; color: ${order_cat.css['color']}; background-color: ${order_cat.css['background-color']};"
                            id="${label_uid}" title="${label_title}"
                            class="label editable">${order_cat.label}
                    </div>
                </td>
                <td class="record-table-date"><input type="color" id="${fgcolor_uid}" class="fgcolor picker"
                                                     title="${fgcolor_title}"
                                                     value="${order_cat.css['color']}"/></td>
                <td class="record-table-date"><input type="color" id="${bgcolor_uid}" class="bgcolor picker"
                                                     title="${bgcolor_title}"
                                                     value="${order_cat.css['background-color']}"/></td>
                <td>
                    <form id="${delete_form_uid}" class="delete_form inline_form"
                          action="${tg.url('/admin/order_cat/{uid}/delete'.format(uid=order_cat.uid))}"
                          method="get">
                        <p>
                            <button id="${delete_form_uid}__delete" type="submit" class="delete_button"
                                    title="${delete_form_title}">${_(u"Supprimer")}
                            </button>
                        </p>
                    </form>
                </td>
            </tr>
            <!--
            %endfor
            -->
            </tbody>
            <tfoot>
            <tr class="droppable">
                <td class="record-table-name">
                    <!-- <%
                    input_title = _(u'Code couleur (ne doit comporter que des lettres)')
                    if cat_group == label:
                        has_error = "code" in form_errors
                        input_cls = "error" if has_error else ""
                        input_val = values.get("code", "")
                    else:
                        has_error = False
                        input_cls = ""
                        input_val = ""
                    %> -->
                    <input type="text" name="code" form="${create_form_uid}"
                           placeholder="CodeCouleur"
                           class="${input_cls}" value="${input_val}" title="${input_title}"/>
                    %if has_error:
                    <br/>
                    <span class="error">${form_errors['code']}</span>
                    %endif
                </td>
                <td class="record-table-label">
                    <!-- <%
                    input_title = _(u'Libellé de la catégorie (requis)')
                    if cat_group == label:
                        has_error =  "label" in form_errors
                        input_cls = "error" if has_error else ""
                        input_val = values.get("label", "")
                    else:
                        has_error = False
                        input_cls = ""
                        input_val = ""
                    %> -->
                    <input type="text" name="label" form="${create_form_uid}"
                           placeholder="Nouvelle catégorie"
                           class="${input_cls}" value="${input_val}" title="${input_title}"/>
                    %if has_error:
                    <br/>
                    <span class="error">${form_errors['label']}</span>
                    %endif
                </td>
                <td class="record-table-date">
                    <!-- <%
                    input_title = _(u'Couleur du texte')
                    if cat_group == label:
                        input_val = values.get("color", "#000000")
                    else:
                        input_val = "#000000"
                    %> -->
                    <input type="color" name="color" form="${create_form_uid}"
                           value="${input_val}" title="${input_title}"/>
                </td>
                <td class="record-table-date">
                    <!-- <%
                    input_title = _(u'Couleur du fond')
                    if cat_group == label:
                        input_val = values.get("background-color", "#ffffff")
                    else:
                        input_val = "#ffffff"
                    %> -->
                    <input type="color" name="background-color" form="${create_form_uid}"
                           value="${input_val}" title="${input_title}"/>
                </td>
                <td>
                    <form id="${create_form_uid}" class="create_form inline_form"
                          action="${tg.url('/admin/order_cat/create_in_place')}"
                          method="post" enctype="multipart/form-data">
                        <p>
                            <input name="cat_group" type="hidden" value="${label}" form="${create_form_uid}"/>
                            <button form="${create_form_uid}" type="submit" class="create_button"
                                    title="${create_form_title}">${_(u"Créer")}
                            </button>
                        </p>
                    </form>
                </td>
            </tr>
            </tfoot>
        </table>
        %if flash and cat_group == label:
        ${flash | n}
        %endif
        %endfor
    </div>

    <script type='text/javascript'><!--
	"use strict";
	/*global $*/

	$(".record-table").styleTable();

	// see: http://vitalets.github.io/x-editable/docs.html
    $('#cat_groups .cat_group.editable').editable({
		type: "text",
		clear: true,
		pk: "unused",
		url: "${tg.url('/admin/order_cat/edit_cat_group')}",
		title: "Saisir le nom du groupe",
		placeholder: "Groupe",
		emptytext: "(sans nom)",
		showbuttons: false,
		onblur: "cancel",
		success: function(response, newValue) {
			if (response.status === 'error') {
				return response.msg;
			}
		},
		inputclass: "input-medium cat_group"
	});
    $('#cat_groups .code.editable').editable({
		type: "text",
		clear: true,
		pk: "unused",
		url: "${tg.url('/admin/order_cat/edit_code')}",
		title: "Saisir le code couleur",
		placeholder: "Color",
		emptytext: "(code vide)",
		showbuttons: false,
		onblur: "cancel",
		success: function(response, newValue) {
			if (response.status === 'error') {
				return response.msg;
			}
		},
		inputclass: "input-medium code"
	});
    $('#cat_groups .label.editable').editable({
		type: "text",
		clear: true,
		pk: "unused",
		url: "${tg.url('/admin/order_cat/edit_label')}",
		title: "Saisir le libellé de la catégorie",
		placeholder: "Libellé",
		emptytext: "(libellé vide)",
		showbuttons: false,
		onblur: "cancel",
		success: function(response, newValue) {
			if (response.status === 'error') {
				return response.msg;
			}
		},
		inputclass: "input-medium label"
	});
    $('#cat_groups .fgcolor.picker').change(function(){
        var data = {name: $(this).attr('id'), value: $(this).val(), pk: "color"};
        $.post("${tg.url('/admin/order_cat/edit_color')}", data);
        $(this).parents("tr").find(".label").css("color", $(this).val());
    });
    $('#cat_groups .bgcolor.picker').change(function(){
        var data = {name: $(this).attr('id'), value: $(this).val(), pk: "background-color"};
        $.post("${tg.url('/admin/order_cat/edit_color')}", data);
        $(this).parents("tr").find(".label").css("background-color",  $(this).val());
    });
    $('#cat_groups .delete_button').button({
        text : false,
        icons : {
            primary : "ui-icon-trash"
        }
    });
    $('#cat_groups .delete_form').ajaxForm({
        target : '#confirm_dialog_content'
    });
    $('#cat_groups .create_button').button({
        text : false,
        icons : {
            primary : "ui-icon-plus"
        }
    });
    $('#cat_groups .create_form').ajaxForm({
        target : '#cat_groups_list'
    });
    $('.draggable').draggable({
		appendTo: '#rightFrame',
		containment: '#rightFrame',
		cursor: 'move',
		delay: 200,
		distance: 5,
		helper: function() {
		    var tbody = $('<tbody></tbody>').append($(this).clone());
		    var table = $('<table class="record-table styleTable drag-selected" ' +
                'style="border: 5px solid #F39814;"></table>').append(tbody);
            return table[0];
		},
		opacity: 0.9,
		revert: 'invalid',  // only if draggable not on droppable
		revertDuration: 300,
		scroll: true,
		scrollSensitivity: 20,
		scrollSpeed: 20,
		start: function(event, ui) {
		    $(this).hide();
		},
//		drag: function(event, ui) {
//        },
		stop: function(event, ui) {
		    $(this).show();
		}
	});
    $('.droppable').droppable({
        accept: ".draggable",
        activeClass: "ui-state-hover",
        hoverClass: "ui-state-active",
        drop: function(event, ui) {
            $(this).find("td").removeClass("ui-state-active");
            ui.draggable.detach().insertBefore($(this));
            // fragid = "order_cat_{0}".format(order_cat.uid)
            var order_cat_uid = ui.draggable[0].id.substring(10);
            var cat_group = $(this).parents("table").prev("h2")[0].innerText;
            var url = "${tg.url('/admin/order_cat/edit_cat_group')}";
            var data = {name: "order_cat__cat_group__" + order_cat_uid,
                        value: cat_group,
                        pk: order_cat_uid};
            $.post(url, data, function(response) {
                if (response.status == "updated") {
                    // response.label == cat_group
                } else if (response.status == "error") {
                    // response.msg == error message: "Can't set group..."
                } else {
                    // unknown response (HTML?)
                }
            });
        },
        over: function(event, ui) {
            $(this).find("td").addClass("ui-state-active");
        },
        out: function(event, ui) {
            $(this).find("td").removeClass("ui-state-active");
        }
    });
-->
    </script>
</div>
