# -*- coding: utf-8 -*-
<!--
<%! import json %>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
-->
<div>
    <form id="order_cat_post_delete" class="ui-widget"
          action="${tg.url('/admin/order_cat/{uid}'.format(uid=order_cat.uid))}"
          method="post">
        %if order_list:
            <!--<%
            sample_size = 5
            sample_list = order_list[:sample_size]
            rest_count = len(order_list[sample_size:])
            %>-->
            %if len(order_list) == 1:
                <p style="margin-bottom: .5em">${_(u"Cette catégorie est utilisée par la commande suivante\u00a0:")}</p>
            %else:
                <p style="margin-bottom: .5em">${_(u"Cette catégorie est utilisée par les {count} commandes suivantes\u00a0:").format(count=len(order_list))}</p>
            %endif
            <ul>
                %for sample in sample_list:
                    <li>${_(u"n°\u00a0{uid}\u00a0:").format(uid=sample.uid)}
                        <a href="${tg.url('/admin/order/index.html?uid={uid}'.format(uid=sample.uid))}">${_(u"{order_ref}").format(order_ref=sample.order_ref)}</a></li>
                %endfor
                %if rest_count > 0:
                    <li><i>${_(u"et {count} autres\u2026").format(count=rest_count)}</i></li>
                %endif
            </ul>
            <p style="margin-bottom: .5em">${_(u"La suppression d’une catégorie utilisée par une commande est sans conséquence. "
                   u"La commande restera attachée au code couleur de la catégorie une fois supprimée.")}</p>
            <p style="margin-bottom: .5em">${_(u"Par la suite, vous pourrez re-créer cette catégorie avec l’ancien code couleur, "
                   u"les commandes concernées reprondront automatiquement les nouvelles couleurs de texte et de fond.")}</p>
        %else:
            <p style="margin-bottom: .5em">Cette catégorie n‘est utilisée par aucune commande.</p>
            <p style="margin-bottom: .5em">Vous pouvez la supprimer sans conséquence.</p>
        %endif
        <input type="hidden" name="_method" value="DELETE"/>
    </form>

    <!--<%
    uid_json = json.dumps(order_cat.uid)
    confirm_dialog_title_fmt = u"Voulez-vous supprimer la catégorie {order_cat_label} ?"
    confirm_dialog_title = confirm_dialog_title_fmt.format(order_cat_label=order_cat.label)
    confirm_dialog_title_json = json.dumps(confirm_dialog_title)
    target_url_json = json.dumps(tg.url('/admin/order_cat.html?display=detail'))
    %>-->
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$('#confirm_dialog').dialog({
		width: 500,
		height: 300,
		buttons: {
			"Supprimer": function() {
				$('#order_cat_post_delete').submit();
				$(this).dialog("close");
			},
			"Annuler": function() {
				$(this).dialog("close");
			}
		},
		title: ${confirm_dialog_title_json|n},
		close: function() {
		}
	}).dialog("open");
	$('#order_cat_post_delete').ajaxForm({
		target : '#confirm_dialog_content',
		success: function(responseText, statusText, xhr) {
            // display full order_cat list, url = /admin/order_cat.html?display=detail
            var target_url = ${target_url_json|n};
            $("#cat_groups_list").load(target_url);
		}
	});
</script>
</div>
