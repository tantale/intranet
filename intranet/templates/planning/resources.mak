##
## La liste des resources est un dict (title => resource_list)
##

<div id="accordion">
    %for title_msg, calendar_list in group_dict.iteritems():
    <h2>${title_msg}</h2>

    <div>
        %if calendar_list:
        %for calendar in calendar_list:
        <%
        checked = 'checked="checked"' if calendar.checked else ''
        fmt = "display: inline-block; width: 12px; height: 12px; border: solid 1px; border-radius: 6px; " \
              "background-color: {calendar.background_color}; " \
              "border-color: {calendar.border_color}; "
        style = fmt.format(calendar=calendar)
        %>\
        <p><input type="checkbox" class="checkbox" name="calendar" id="calendar_${calendar.uid}" ${checked}
                  title="${calendar.description}"/><label
                class="edit_button"
                for="calendar_${calendar.uid}" title="${calendar.description}"><span style="${style}"></span> ${calendar.label}</label>
        </p>
        %endfor
        %else:
        <p>${empty_msg}</p>
        %endif
    </div>
    %endfor
</div>

<script type="text/javascript">
$(function() {
    $('#accordion').accordion({
        collapsible: false,
        heightStyle: "content"
    });
    $("#accordion .checkbox").button().click(function(event) {
        var uid = this.id.split("_")[1], checked = this.checked;
        var tz_offset = new Date().getTimezoneOffset();
        jQuery.ajax("./resources", {method: "put", data: {uid: uid, checked: checked}});
        var url = "./sources/" + uid + "?tz_offset=" + encodeURIComponent(tz_offset);
        jQuery.getJSON(url, function( eventSource ) {
            var action = (checked == true) ? 'addEventSource' : 'removeEventSource';
            $('#event_sources').fullCalendar(action, eventSource);
        });
    });
});
</script>