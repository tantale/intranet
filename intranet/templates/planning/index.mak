<%inherit file="local:templates.pointage.master"/>

<%def name="title()">${_(u"Planning des événements")}</%def>

<%def name="search_frame()">
</%def>

<%def name="new_frame()">
</%def>

<%def name="accordion_content()">
<div id="planning_resources">
    <img src="/images/editable/loading.gif" alt="Chargement en cours"/>
    Chargement des employés…
</div>
</%def>

<%def name="content_frame()">
<div id="planning_calendar">
    <img src="/images/editable/loading.gif" alt="Chargement en cours"/>
    Chargement du calendrier…
</div>
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
                },
                center__onresize : function(name, element, state, options, layout_name) {
                    $('#calendar').fullCalendar('render');
                }}));
        });

        $('#confirm_dialog').dialog({
            autoOpen: false,
            width: 400,
            height: 200,
            modal: true
        });

        var tz_offset = new Date().getTimezoneOffset();
        $('#planning_resources').load("./resources");
        $('#planning_calendar').load("./sources?tz_offset=" + encodeURIComponent(tz_offset));
	});

</script>
</%def>
