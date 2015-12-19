<%namespace file="intranet.templates.planning.calendar.ctrl_select_class_name" import="select_class_name"/>
<!--
<%flash = tg.flash_obj.render('flash', use_js=False)%>
-->
<article id="calendar_new">
    <form id="calendar_new_create_form" class="create_form"
          action="${tg.url('/admin/planning/calendar/')}"
          method="post" enctype="multipart/form-data">
        <h2>
            <!-- <%
            input_name = "label"
            input_title = _(u'Libellé du calendrier (il doit être unique)')
            input_placeholder = _(u'Libellé')
            has_error = input_name in form_errors
            input_cls = "error" if has_error else ""
            input_val = values.get(input_name, "")
            %> -->
            <input type="text"
                   name="${input_name}" title="${input_title}" placeholder="${input_placeholder}"
                   class="${input_cls} label" value="${input_val}"/>
            %if has_error:
            <br/>
            <span class="error">${form_errors[input_name]}</span>
            %endif
        </h2>

        <p>
            <!-- <%
            input_name = "description"
            input_title = _(u'Description du calendrier, contexte d’utilisation, etc.')
            input_placeholder = _(u'Description du calendrier')
            has_error = input_name in form_errors
            input_cls = "error" if has_error else ""
            input_val = values.get(input_name, "")
            %> -->
            <textarea
                    name="${input_name}" title="${input_title}" placeholder="${input_placeholder}"
                    class="${input_cls} description">${input_val}</textarea>
            %if has_error:
            <br/>
            <span class="error">${form_errors[input_name]}</span>
            %endif
        </p>

        <p>
            <label for="calendar_new_week_hours_uid">Horaires applicables&nbsp;: </label>
            <!-- <%
            input_name = "week_hours_uid"
            input_title = _(u'Attribuer un calendrier à un employé')
            input_val = values.get(input_name, "")
            %> -->
            <select id="calendar_new_week_hours_uid"
                    class="ui-widget ui-state-default ui-corner-all"
                    name="${input_name}" title="${input_title}">
                %for week_hours in week_hours_list:
                %if input_val == week_hours.uid:
                <option value="${week_hours.uid}" selected="selected">${week_hours.label}</option>
                %else:
                <option value="${week_hours.uid}">${week_hours.label}</option>
                %endif
                %endfor
            </select>
        </p>

        <details>
            <summary>Couleurs et style</summary>
            <table border="0">
                <tbody>
                <tr>
                    <td><label for="calendar_new_background_color">fond&nbsp;: </label></td>
                    <td><input id="calendar_new_background_color" class="background_color" type="color"
                               name="background_color" title="${_(u'Couleur du fond')}"
                               value="${values.get('background_color')}"/>
                    </td>
                </tr>
                <tr>
                    <td><label for="calendar_new_border_color">bordures&nbsp;: </label></td>
                    <td><input id="calendar_new_border_color" class="border_color" type="color"
                               name="border_color" title="${_(u'Couleur des bordures')}"
                               value="${values.get('border_color')}"/>
                    </td>
                </tr>
                <tr>
                    <td><label for="calendar_new_text_color">texte&nbsp;: </label></td>
                    <td><input id="calendar_new_text_color" class="text_color" type="color"
                               name="text_color" title="${_(u'Couleur du texte')}" value="${values.get('text_color')}"/>
                    </td>
                </tr>
                <tr>
                    <td><label for="calendar_new_groups">catégorie&nbsp;: </label></td>
                    <td>${select_class_name("calendar_new_groups",
                        "class_name", _(u"Sélectionnez une catégorie"),
                        order_cat_groups, selected_cat_name=values.get('class_name'), empty_label=_(u"(Aucune)"))}
                    </td>
                </tr>
                </tbody>
            </table>

        </details>
        <nav>
            <p>
                <button id="calendar_new_create" type="submit" class="create_button"
                        title="Ajouter un nouveau calendrier">${_(u"Créer")}
                </button>
            </p>
        </nav>
        %if flash:
        ${flash | n}
        %endif
    </form>
</article>
<script type='text/javascript'><!--
    "use strict";
    /*global $*/
    $(function() {
        $('#calendar_new_create_form .create_button').button({
            text : true,
            icons : {
                primary : "ui-icon-plus"
            }
        });
        $('#calendar_new_create_form').ajaxForm({
            target : '#calendar footer',
            success:    function() {
                $('#calendar section').load("${tg.url('/admin/planning/calendar/get_all')}");
                $('#flash').toggle("fade", "easeInExpo", 3000);
            }
        });
    });
-->
</script>
