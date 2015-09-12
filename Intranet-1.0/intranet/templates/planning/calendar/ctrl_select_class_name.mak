<%def name="select_class_name(id, name, title, order_cat_groups, selected_cat_name='', empty_label='(aucun)', form='')">
<select id="${id}" name="${name}" title="${title}" class="${selected_cat_name}" form="${form}">
    ##
    ## Empty option: if selected_cat_name == "", mark the empty option as selected
    ##
    %if selected_cat_name:
    <option value="" class="noColor">${empty_label}</option>
    %else:
    <option selected="selected" value="" class="noColor">${empty_label}</option>
    %endif
    ##
    ## Groups
    ##
    %for cat_group, order_cat_list in order_cat_groups.iteritems():
    <optgroup label="${cat_group}" class="noColor">
        %for order_cat in order_cat_list:
        %if order_cat.cat_name == selected_cat_name:
        <option selected="selected"
                class="${order_cat.cat_name}"
                value="${order_cat.cat_name}">${order_cat.label}
        </option>
        %else:
        <option
                class="${order_cat.cat_name}"
                value="${order_cat.cat_name}">${order_cat.label}
        </option>
        %endif
        %endfor
    </optgroup>
    %endfor
</select>
</%def>
