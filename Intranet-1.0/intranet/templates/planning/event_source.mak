<h2>Planning</h2>

<pre>${eventSources|n}</pre>

<div id='event_source'><!-- event_source placeholder --></div>

<script type='text/javascript'>
	"use strict";
	/*global $*/

    jQuery.get("./full_calendar.json", function(data) {

        var prop = {
            viewRender: function( view, element ) {
                var currDate = $("#event_source").fullCalendar('getDate');
                var ajaxData = {
                    defaultView : view.name,
                    date : currDate.getDate(),
                    month : currDate.getMonth(),
                    year : currDate.getFullYear()
                };
                console.debug("event_source.full_calendar put:", ajaxData);
                jQuery.ajax("./full_calendar", { method : "put", data : ajaxData });
            },
            eventSources: ${eventSources|n}
        };

        $('#event_source').fullCalendar($.extend(data, prop));

    });
</script>