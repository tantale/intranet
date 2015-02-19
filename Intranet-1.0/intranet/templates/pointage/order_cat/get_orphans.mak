<!--
<%
flash = tg.flash_obj.render('flash', use_js=False)
curr_code = values.get("code")
%>
-->
<div>
<div id="orphans_groups">
%if flash and not curr_code:
${flash | n}
%endif
%if orphans_groups:
    ## -- Prepare the list of all categories groups
    <datalist id="cat_groups">
        %for cat_group in cat_group_index.iterkeys():
        <option value="${cat_group}"/>
        %endfor
    </datalist>

    ## -- each orphans group contains a non empty list of orders
    %for code, orphans in orphans_groups.iteritems():
        <div id="orphans__${code}">
        <!--<%
            create_form_title = _(u"Créer un nouveau groupe et une nouvelle catégorie")
        %>-->
        <form class="orphan_create"
              action="${tg.url('/admin/order_cat/post_orphan')}"
              method="post" enctype="multipart/form-data">

        <!-- <%
        input_title = _(u'Nom du groupe de catégories')
        has_error = curr_code == code and "cat_group" in form_errors
        input_val = values.get("cat_group", "")
        %> -->
        <h2><label for="orphan_create__${code}__cat_group">${_(u"Groupe")} :</label>
            <input id="orphan_create__${code}__cat_group" list="cat_groups" name="cat_group"
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
                    input_title = _(u'Code couleur : {code}').format(code=code)
                    %> -->
                    <input type="text" name="code"
                           readonly="true"
                           value="${code}" title="${input_title}"/>
                </td>
                <td class="record-table-label">
                    <!-- <%
                    input_title = _(u'Libellé de la catégorie (requis)')
                    has_error = curr_code == code and "label" in form_errors
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

        %if flash and curr_code == code:
        ${flash | n}
        %endif

        <!--<%
        sample_size = 5
        sample_list = orphans[:sample_size]
        rest_count = len(orphans[sample_size:])
        %>-->
        %if len(orphans) == 1:
            <p style="margin-bottom: .5em">${_(u"Cette catégorie est utilisée par la commande suivante\u00a0:")}</p>
        %else:
            <p style="margin-bottom: .5em">${_(u"Cette catégorie est utilisée par les {count} commandes suivantes\u00a0:").format(count=len(orphans))}</p>
        %endif
        <ul>
            %for sample in sample_list:
                <li>${_(u"n°\u00a0{uid}\u00a0:").format(uid=sample.uid)}
                    <a href="${tg.url('/admin/order/index.html?uid={uid}'.format(uid=sample.uid))}">${_(u"{order_ref}").format(order_ref=sample.order_ref)}</a></li>
            %endfor
            %if rest_count > 0:
                <li><i>${_(u"et {count} autres\u2026").format(count=rest_count)}</i></li>
            %endif
        </ul>

        </form>

        </div>
    %endfor
%else:
    ## -- no orphans at all
    <h2>${_(u"(aucune commande sans catégorie)")}</h2>
%endif
</div>
<script type='text/javascript'><!--
	$(".record-table").styleTable();
    $('.orphan_create').ajaxForm({
        target : '#prefs_content',
        beforeSubmit: function(arr, form, options) {
            $('#flash').hide();
        }
    });
    $('.orphan_create .create_button').button({
		text : false,
		icons : {
			primary : "ui-icon-check"
		}
    });
--></script>
</div>