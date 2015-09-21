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
        %>\
        <p><input type="checkbox" class="checkbox" name="calendar" id="calendar_${calendar.uid}" ${checked}
                  title="${calendar.description}"/><label
                class="edit_button"
                for="calendar_${calendar.uid}" title="${calendar.description}">${calendar.label}</label>
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
        var uid = this.id.split("_")[1];
        jQuery.ajax("./resources", {method: "put", data: {uid: uid, checked: this.checked}});
    });
});




</script>