<!--
## result = dict(week_hours_uid=self.week_hours_uid, day_period=day_period)
<%
post_delete_url = tg.url('/admin/planning/week_hours/{0}/day_periods/{1}'.format(week_hours_uid, day_period.uid))
%>
-->
<form id="day_period_post_delete" class="ui-widget" action="${tg.url(post_delete_url)}" method="post">

    <p style="margin-bottom: .75em">Voulez vous supprimer la plage horaire «&nbsp;${day_period.label}&nbsp;»&nbsp;?</p>

    %if day_period.hours_interval_list:
    <p style="margin-bottom: .2em">Cette plage horaire comprend les heures suivants&nbsp;:</p>
    <ul>
    %for hours_interval in day_period.hours_interval_list:
    	<li style="margin-bottom: .2em">${hours_interval.week_day.label}&nbsp;: de&nbsp;${hours_interval.start_hour.strftime("%H:%M")} à&nbsp;${hours_interval.end_hour.strftime("%H:%M")}</li>
    %endfor
	</ul>
    %else:
    <p style="margin-bottom: .2em">Cette plage horaire ne comprend pas d’heure.</p>
    %endif

    <input type="hidden" name="_method" value="DELETE"/>
</form>
<script type='text/javascript'><!--
"use strict";
/*global $*/
$(function() {
    $('#day_period_post_delete').ajaxForm({
        target : '#confirm_dialog_content',
        success: function(responseText, statusText, xhr) {
        	// Reload all!
        	$('#week_hours section').load("${tg.url('/admin/planning/week_hours/get_all')}");
        }
    });
});
-->
</script>
