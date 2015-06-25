##
## La liste des resources est un dict (title => resource_list)
##

<div id="accordion">
    %for title_msg, employee_list in group_dict.iteritems():
    <h2>${title_msg}</h2>

    <div>
        %if employee_list:
        %for employee in employee_list:
        <%
        img_src = employee.photo_path if employee.photo_path else tg.url('/images/silhouette.min.png')
        checked = 'checked="checked"' if employee.checked else ''
        %>\
        <p><input type="checkbox" class="checkbox" name="employee" id="employee_${employee.uid}" ${checked}
                  title="${employee.employee_name}"
                /><label
                class="edit_button"
                for="employee_${employee.uid}"><img class="valignMiddle picture_box_inner_min"
                                                    alt="${employee.employee_name} - Photo"
                                                    src="${img_src}"/>${employee.employee_name}</label>
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