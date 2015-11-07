<%def name="day_period_label(week_hours_uid, day_period)">
<!--
## result = dict(week_hours_uid=self.week_hours_uid, day_period=day_period)
<%
article_id = "week_hours_{0}".format(week_hours_uid)
day_period_id = "week_hours_{0}_day_period_{1}".format(week_hours_uid, day_period.uid)
placeholder_id = "week_hours_{0}_day_period_{1}_placeholder".format(week_hours_uid, day_period.uid)
get_delete_url = tg.url('/admin/planning/week_hours/{0}/day_periods/{1}/delete'.format(week_hours_uid, day_period.uid))
get_delete_title = u'Supprimer la plage horaire « {label} »'.format(label=day_period.label)
edit_url = tg.url('/admin/planning/week_hours/{0}/day_periods/edit_in_place'.format(week_hours_uid, day_period.uid))
edit_title = u'Modifier le libellé « {label} »'.format(label=day_period.label)
%>
-->
<a class="delete_button_icon"
   title="${get_delete_title}"
   href="${get_delete_url}">-</a>
<span id="${day_period_id}_label" class="day_period_label editable"
	  title="${edit_title}">${day_period.label}</span>
<script type='text/javascript'>
    "use strict";
    /*global $*/
    $(function() {
        $(".delete_button_icon").button({
            text : false,
            icons : {
                primary : "ui-icon-trash"
            }
        }).click(function(event){
            event.preventDefault();
            var url = $(this).attr("href");
            $('#confirm_dialog_content').load(url, function(){
		        $('#confirm_dialog').dialog({
		            width: 500,
		            height: 300,
		            buttons: {
		                "Supprimer": function() {
		                    $('#day_period_post_delete').submit();
		                    $(this).dialog("close");
		                },
		                "Annuler": function() {
		                    $(this).dialog("close");
		                }
		            },
		            title: "${get_delete_title|n}",
		            close: function() {
		            }
		        }).dialog("open");
            });
        });
        $('.day_period_label.editable').editable({
            type: "text",
            clear: true,
            pk: "unused",
            url: "${tg.url(edit_url)}",
            title: "${edit_title|n}",
            placeholder: "Libellé",
            emptytext: "(vide)",
            showbuttons: false,
            onblur: "cancel",
            error: function(response, newValue) {
                response = JSON.parse(response.responseText);
                return response.msg;
            },
            inputclass: "input-medium code"  // intranet-pointage.css
        });
    })
</script>
</%def>
