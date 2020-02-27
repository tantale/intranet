<!--
<%flash = tg.flash_obj.render('flash', use_js=False)%>
-->
<article id="week_hours_new">
    <form id="week_hours_new_create_form" class="create_form"
          action="${tg.url('/admin/planning/week_hours/')}"
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

        <nav>
            <p>
                <button id="week_hours_new_create" type="submit" class="create_button"
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
        $('#week_hours_new_create_form .create_button').button({
            text : true,
            icons : {
                primary : "ui-icon-plus"
            }
        });
        $('#week_hours_new_create_form').ajaxForm({
            target : '#week_hours footer',
            success:    function() {
                $('#week_hours section').load("${tg.url('/admin/planning/week_hours/get_all')}");
                $('#flash').toggle("fade", "easeInExpo", 3000);
            }
        });
    });
-->
</script>
