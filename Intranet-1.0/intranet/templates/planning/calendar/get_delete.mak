# -*- coding: utf-8 -*-
<!--
<%! import json %>
-->
<div>
    <form id="calendar_post_delete" class="ui-widget"
          action="${tg.url('/admin/planning/calendar/{uid}'.format(uid=calendar.uid))}"
          method="post">
        <p style="margin-bottom: .5em">Ce calendrier ne contient pas d’événement.</p>

        <p style="margin-bottom: .5em">Vous pouvez le supprimer sans conséquence.</p>
        <input type="hidden" name="_method" value="DELETE"/>
    </form>
    <!--<%
    uid_json = json.dumps(calendar.uid)
    confirm_dialog_title_fmt = u"Voulez-vous supprimer le calendrier {label} ?"
    confirm_dialog_title = confirm_dialog_title_fmt.format(label=calendar.label)
    confirm_dialog_title_json = json.dumps(confirm_dialog_title)
    %>-->
    <script type='text/javascript'><!--
	"use strict";
	/*global $*/
    $(function() {
        $('#confirm_dialog').dialog({
            width: 500,
            height: 300,
            buttons: {
                "Supprimer": function() {
                    $('#calendar_post_delete').submit();
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
        $('#calendar_post_delete').ajaxForm({
            target : '#confirm_dialog_content',
            success: function(responseText, statusText, xhr) {
                $("#calendar_${calendar.uid}").remove();
            }
        });
    });
    -->
    </script>
</div>
