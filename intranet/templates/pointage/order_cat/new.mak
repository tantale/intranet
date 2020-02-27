<div>
    <div id="order_cat_create_content">
    <!--<%
        create_form_title = _(u"Créer un nouveau groupe et une nouvelle catégorie")
    %>-->
    <form id="order_cat_create" class="XXXui-widget"
          action="${tg.url('/admin/order_cat/')}"
          method="post" enctype="multipart/form-data">

    <!-- <%
    input_title = _(u'Nom du groupe de catégories')
    has_error = "cat_group" in form_errors
    input_val = values.get("cat_group", "")
    %> -->
    <h2><label for="order_cat_create__cat_group">${_(u"Nouveau groupe")} :</label>
        <input id="order_cat_create__cat_group" type="text" name="cat_group"
                       placeholder="Mon groupe"
                       value="${input_val}" title="${input_title}"/>
        %if has_error:
        <span class="error">${form_errors['cat_group']}</span>
        %endif
    </h2>

    <table class="record-table" style="page-break-inside: avoid">
        <thead>
        <tr>
            <th class="record-table-name">${_(u"Code couleur")}</th>
            <th class="record-table-label">${_(u"Libellé")}</th>
            <th class="record-table-name">${_(u"Couleur du texte")}</th>
            <th class="record-table-name">${_(u"Couleur du fond")}</th>
            <th><!--empty--></th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td class="record-table-name">
                <!-- <%
                input_title = _(u'Code couleur (ne doit comporter que des lettres)')
                has_error = "code" in form_errors
                input_cls = "error" if has_error else ""
                input_val = values.get("code", "")
                %> -->
                <input type="text" name="code"
                       placeholder="CodeCouleur"
                       class="${input_cls}" value="${input_val}" title="${input_title}"/>
                %if has_error:
                <br/>
                <span class="error">${form_errors['code']}</span>
                %endif
            </td>
            <td class="record-table-label">
                <!-- <%
                input_title = _(u'Libellé de la catégorie (requis)')
                has_error =  "label" in form_errors
                input_cls = "error" if has_error else ""
                input_val = values.get("label", "")
                %> -->
                <input type="text" name="label"
                       placeholder="Nouvelle catégorie"
                       class="${input_cls}" value="${input_val}" title="${input_title}"/>
                %if has_error:
                <br/>
                <span class="error">${form_errors['label']}</span>
                %endif
            </td>
            <td class="record-table-date">
                <!-- <%
                input_title = _(u'Couleur du texte')
                input_val = values.get("color", "#000000")
                %> -->
                <input type="color" name="color"
                       value="${input_val}" title="${input_title}"/>
            </td>
            <td class="record-table-date">
                <!-- <%
                input_title = _(u'Couleur du fond')
                input_val = values.get("background-color", "#ffffff")
                %> -->
                <input type="color" name="background-color"
                       value="${input_val}" title="${input_title}"/>
            </td>
            <td>
                <button type="submit" class="create_button"
                        title="${create_form_title}">${_(u"Créer")}
                </button>
            </td>
        </tr>
        </tbody>
    </table>
    </form>
</div>
<script type='text/javascript'><!--
	$(".record-table").styleTable();
    $('#order_cat_create').ajaxForm({
        target : '#cat_groups_new',
        beforeSubmit: function(arr, form, options) {
            $('#flash').hide();
        },
        success: function(responseJson, statusText, xhr) {
            $('#cat_groups_list').load("/admin/order_cat/get_all.html");
        }
    });
    $('#order_cat_create .create_button').button({
		text : false,
		icons : {
			primary : "ui-icon-check"
		}
    });
--></script>
</div>
