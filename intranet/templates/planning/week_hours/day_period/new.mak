<!--
<%
article_id = "week_hours_{0}".format(week_hours_uid)
form_id = "{0}_day_period_new_form".format(article_id)
form_action = tg.url('/admin/planning/week_hours/{0}/day_periods/'.format(week_hours_uid))
target_id = "{0}_new_day_period".format(article_id);
%>
-->
<form id="${form_id}" class="inline_form" action="${form_action}" method="post" enctype="multipart/form-data">
    %if flash:
    ${flash | n}
    %endif
    <label><input type="text" name="label" autocomplete="off"
                  title="Libellé de la plage horaire (requis)"
                  placeholder="Plage horaire" class="label" value="${values.get('label')}"></label>
    %if 'label'in form_errors:
    <br/>
    <span class="error">${form_errors['label']}</span>
    %endif
    <button class="new_button_icon" title="${u'Ajouter les plages horaires'}" type="submit">+</button>
</form>
<script type='text/javascript'>
    "use strict";
    /*global $*/
    $(function() {
        $('#${form_id}').ajaxForm({
            target : '#${target_id}',
            beforeSubmit: function(arr, form, options) {
                $('#flash').hide();
            },
            success: function(responseText, statusText, xhr) {
                // <span class="error">
                var error = $('<div/>').append(responseText).find('span.error');
                if (error.length) {
                    console.log("ERROR: don't update the week_hours.");
                } else {
                   $('#week_hours section').load("${tg.url('/admin/planning/week_hours/get_all')}"); 
                }
            }
        });
    })
</script>