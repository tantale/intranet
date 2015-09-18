# -*- coding: utf-8 -*-
<!--
<%! import json %>
-->
<div>
    <form id="week_hours_post_delete" class="ui-widget"
          action="${tg.url('/admin/planning/week_hours/{uid}'.format(uid=week_hours.uid))}"
          method="post">
        <!--<% calendar_set = set(week_hours.calendar_list + [yp.calendar for yp in week_hours.year_period_list])%>-->
        %if len(calendar_set) == 0:
        <p style="margin-bottom: .5em">Cette grille d’horaires n’est associée à aucun calendrier.</p>
        %elif len(calendar_set) == 1:
        <p style="margin-bottom: .5em">Cette grille d’horaires est associée à 1 calendrier&nbsp:</p>
        %else:
        <p style="margin-bottom: .5em">Cette grille d’horaires est associée à ${len(calendar_set)} calendriers&nbsp;</p>
        %endif

        %if calendar_set:
        <ul style="list-style-type:none">
            %for calendar in sorted(calendar_set, key=lambda cal: cal.position):
                <li>${calendar.uid}&nbsp;: ${calendar.label}</li>
            %endfor
        </ul>
        %endif

        %if calendar_set:
        <p style="margin-bottom: .5em">Vous ne pouvez pas supprimer ces horaires.</p>
        %else:
        <p style="margin-bottom: .5em">Vous pouvez supprimer ces horaires.</p>
        %endif

        <input type="hidden" name="_method" value="DELETE"/>
    </form>
    <!--<%
    uid_json = json.dumps(week_hours.uid)
    confirm_dialog_title_fmt = u"Voulez-vous supprimer « {label} » ?"
    confirm_dialog_title = confirm_dialog_title_fmt.format(label=week_hours.label)
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
%if calendar_set:
                "OK": function() {
                    $(this).dialog("close");
                }
%else:
                "Supprimer": function() {
                    $('#week_hours_post_delete').submit();
                    $(this).dialog("close");
                },
                "Annuler": function() {
                    $(this).dialog("close");
                }
%endif
            },
            title: ${confirm_dialog_title_json|n},
            close: function() {
            }
        }).dialog("open");
        $('#week_hours_post_delete').ajaxForm({
            target : '#confirm_dialog_content',
            success: function(responseText, statusText, xhr) {
                $("#week_hours_${week_hours.uid}").remove();
            }
        });
    });
    -->
    </script>
</div>
