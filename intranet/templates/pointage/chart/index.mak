<%inherit file="local:templates.pointage.master"/>

<%def name="title()">${_(u"Statistiques des pointages")}</%def>

<%def name="search_frame()">
<form id="search_get_all" class="ui-state-default"
      action="${tg.url('./get_all/')}" method="get">

    <div class="ui-widget">

        <style type="text/css" scoped="scoped">
            table.selection            {margin: 0 auto 0 auto;}
            table.selection td         {font-size: .8em;}
        </style>

        <table class="selection">
            <tbody>

            <tr>
                <td><label for="search_get_all__uid">${_(u'N° commande :')}</label></td>
                <td><input id="search_get_all__uid"
                           type="search" name="uid"
                           title="${_(u'Numéro de la commande')}"/></td>
            </tr>

            <tr>
                <td><label for="search_get_all__order_ref">${_(u'Ref. commande :')}</label></td>
                <td><input id="search_get_all__order_ref"
                           type="search" name="order_ref"
                           title="${_(u'Référence de la commande')}"/></td>
            </tr>

            <tr>
                <td><label for="search_get_all__project_cat">${_(u'Catégorie de projet :')}</label></td>
                <td><select id="search_get_all__project_cat" name="project_cat"
                            title="Catégorie de projet">
                    <option selected="selected" value="">(toutes)</option>
                    %if cat_dict:
                    %for cat_group, order_cat_list in cat_dict.iteritems():
                    <optgroup label="${cat_group}" class="noColor">
                        %for order_cat in order_cat_list:
                        <option
                                class="${order_cat.cat_name}"
                                value="${order_cat.cat_name}">${order_cat.label}
                        </option>
                        %endfor
                    </optgroup>
                    %endfor
                    %else:
                    <!-- not cat_dict ==> use missing_order_cat_label -->
                    <option selected="selected">${missing_order_cat_label}</option>
                    %endif
                </select></td>
            </tr>
            <tr>
                <td><label for="search_get_all__start_date">${_(u'Date de début :')}</label></td>
                <td><input id="search_get_all__start_date" type="date" name="start_date"
                           title="${_(u'Date de début de recherche')}"/></td>
            </tr>

            <tr>
                <td><label for="search_get_all__end_date">${_(u'Date de fin :')}</label></td>
                <td><input id="search_get_all__end_date" type="date" name="end_date"
                           title="${_(u'Date de fin de recherche')}"/></td>
            </tr>

            <tr>
                <td><label for="search_get_all__closed">${_(u'Statut :')}</label></td>
                <td><select id="search_get_all__closed" name="closed"
                            title="${_(u'Statut de la commande (clôturée ou non)')}">
                    <option value="">${_(u'Indifférent')}</option>
                    <option value="true">${_(u'Clôturée')}</option>
                    <option value="false">${_(u'Non clôturée')}</option>
                </select></td>
            </tr>
            </tbody>
            <tfoot>
            <tr>
                <td colspan="2" align="center">
                    <button id="search_get_all__search" type="submit" class="search_button"
                            title="${_(u'Rechercher / filtrer selon les critères')}">${_(u"Rechercher")}
                    </button>
                </td>
            </tr>
            </tfoot>
        </table>
    </div>
</form>
</%def>

<%def name="new_frame()">
</%def>

<%def name="accordion_content()">
</%def>

<%def name="content_frame()">
<div id="chart_content"></div>
</%def>

<%def name="extra_scripts()">
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(function() {
        jQuery.get("./layout.json", function(data){
            $('body').layout($.extend(data, {
                west__onresize : function(name, element, state, options, layout_name) {
                    jQuery.ajax("./layout", {method: "put", data: {west__size: state.size}});
                }}));
        });
		$('#accordion').accordion({
			collapsible: false,
			heightStyle: "content"
		});
		$('#search_get_all').ajaxForm({
			target: '#chart_content',
			beforeSubmit: function() {
			    $('#chart_content').fadeOut(500);
			},
			success: function() {
			    $('#chart_content').fadeIn("fast");
			}
		});
		$('#confirm_dialog').dialog({
			autoOpen: false,
			width: 400,
			height: 200,
			modal: true
		});
        var project_cat_css = $('#search_get_all__project_cat').val();
        $('#search_get_all__project_cat').change(function(){
            var new_css = $(this).find('option:selected').attr('class');
            $(this).removeClass(project_cat_css).addClass(new_css);
            project_cat_css = new_css;
        });
	});

</script>
</%def>
