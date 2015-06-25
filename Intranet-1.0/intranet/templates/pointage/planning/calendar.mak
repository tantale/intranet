<h2>Planning des employés</h2>

<div id='calendar'><!-- calendar placeholder --></div>

<script type='text/javascript'>
	"use strict";
	/*global $*/

    jQuery.get("./full_calendar.json", function(data) {

        var prop = {
            viewRender: function( view, element ) {
                var currDate = $("#calendar").fullCalendar('getDate');
                var ajaxData = {
                    defaultView : view.name,
                    date : currDate.getDate(),
                    month : currDate.getMonth(),
                    year : currDate.getFullYear()
                };
                console.debug("calendar.full_calendar put:", ajaxData);
                jQuery.ajax("./full_calendar", { method : "put", data : ajaxData });
            },
            eventSources: ${eventSources|n}
        };

        $('#calendar').fullCalendar($.extend(data, prop));

    });
</script>