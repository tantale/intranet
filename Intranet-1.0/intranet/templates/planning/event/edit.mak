<% flash = tg.flash_obj.render('flash', use_js=False) %>
<article>
    <form id="event_edit_form" class="create_form"
          action="${'./sources/events/{uid}'.format(**values)}"
          method="post" enctype="multipart/form-data">
        %if flash:
        ${flash | n}
        %endif
        <p style="display: none; visibility: hidden;">
            <input name="tz_offset" type="hidden" value="${tz_offset}">
            <input type="hidden" name="editable" value="true">
            <input type="hidden" name="_method" value="PUT">
        </p>
        <p>
            %if not calendar_list:
            <span class="error">Aucun calendrier</span>
            %else:
            <label>Calendrier de&nbsp;:
                <select class="ui-widget ui-state-default ui-corner-all" name="calendar_uid"
                        title="Sélectionner le calendrier">
                    %for calendar in calendar_list:
                    %if calendar.uid == values.get('calendar_uid'):
                    <option value="${calendar.uid}" selected="selected">${calendar.label}</option>
                    %else:
                    <option value="${calendar.uid}">${calendar.label}</option>
                    %endif
                    %endfor
                </select></label>
            %endif
        </p>
        <h2>
            <label><input type="text" name="label"
                          title="Libellé de l’événement (requis)"
                          placeholder="Libellé" class="label" value="${values.get('label')}"></label>
            %if values.get('private') == "true":
            <label>Privé&nbsp;:<input type="checkbox" name="private" value="true"
                                      title="Cocher si l’événement est d’ordre privé"
                                      checked="checked"></label>
            %else:
            <label>Privé&nbsp;:<input type="checkbox" name="private" value="true"
                                      title="Cocher si l’événement est d’ordre privé"></label>
            %endif
            %if 'label'in form_errors:
            <br/>
            <span class="error">${form_errors['label']}</span>
            %endif
        </h2>

        <p>
            <textarea name="description"
                      title="Description de l’événement"
                      placeholder="Description de l’événement"
                      class="description">${values.get('description')}</textarea>
            %if 'description'in form_errors:
            <br/>
            <span class="error">${form_errors['description']}</span>
            %endif
        </p>

        <p>
            <textarea name="location"
                      title="Lieu / adresse"
                      placeholder="Lieu ou adresse de l’événement"
                      class="location">${values.get('location')}</textarea>
            %if 'location'in form_errors:
            <br/>
            <span class="error">${form_errors['location']}</span>
            %endif
        </p>

        <p>
            <label>Du&nbsp;<input type="datetime-local" name="event_start"
                                  title="Date/Heure de début"
                                  step="900"
                                  value="${values.get('event_start')}"></label>
            <label>au&nbsp;<input type="datetime-local" name="event_end"
                                  title="Date/Heure de début"
                                  step="900"
                                  value="${values.get('event_end')}"></label>
            %if 'event_start'in form_errors:
            <br/>
            <span class="error">${form_errors['event_start']}</span>
            %endif
            %if 'event_end'in form_errors:
            <br/>
            <span class="error">${form_errors['event_end']}</span>
            %endif
        </p>

        <p>
            %if values.get('all_day') == "true":
            <label>Journée entière&nbsp;:<input type="checkbox" name="all_day" value="true"
                                                title="Cocher si l’événement dure toute une journée ou plus"
                                                checked="checked"></label>
            %else:
            <label>Journée entière&nbsp;:<input type="checkbox" name="all_day" value="true"
                                                title="Cocher si l’événement dure toute une journée ou plus"></label>
            %endif
        </p>
    </form>

    <form id="event_delete_form" class="minimal_form"
          action="${'./sources/{calendar_uid}/events/{uid}'.format(**values)}"
          method="post">
        <p style="display: none; visibility: hidden;">
            <input type="hidden" name="_method" value="DELETE" />
        </p>
    </form>

</article>
<script type='text/javascript'>
    "use strict";
    /*global $*/
    $('#event_edit_form').ajaxForm({
        target : '#confirm_dialog_content',
        beforeSubmit: function(arr, form, options) {
            $('#flash').hide();
        },
        success: function(responseText, statusText, xhr) {
            var error = $('<div/>').append(responseText).find('div.error');
            if (error.length) {
                // keep '#confirm_dialog' opened
                console.log("ERROR: don't update the calendar.");
            } else {
                var event_obj = jQuery.parseJSON(responseText);
                console.log("edit_event", event_obj);
                var start = $.fullCalendar.parseISO8601(event_obj.start);
                $('#confirm_dialog').dialog("close");
                $('#event_sources')
                    .fullCalendar('refetchEvents')
                    .fullCalendar('gotoDate', start);
            }
        }
    });
    function setupEventEnd() {
        var checked = $('#event_edit_form input[name="all_day"]').prop("checked");
        var label = $('#event_edit_form input[name="event_end"]').parents("label");
        if (checked) {
            label.hide();
        } else {
            label.show();
        }
    }
    $('#event_edit_form').ready(setupEventEnd);
    $('#event_edit_form input[name="all_day"]').click(setupEventEnd);
    $('#event_delete_form').ajaxForm({
        target : '#confirm_dialog_content',
        beforeSubmit: function(arr, form, options) {
            $('#flash').hide();
        },
        success: function(responseText, statusText, xhr) {
            var deleted_event = jQuery.parseJSON(responseText);
            $('#confirm_dialog').dialog("close");
            $('#event_sources').fullCalendar('refetchEvents');
        }
    });
</script>