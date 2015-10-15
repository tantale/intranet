<style scoped="scoped">
    article {
        padding-bottom: 1em;
    }
    article p {
        margin: 0.3em 0 .5em 0;
    }
    article h2 .label {
        font-family: arial;
        font-size: 1em;
        font-weight: bold;
        width: 14em;
    }
    article p .description {
        font-family: arial;
        font-size: 1em;
        width: 36em;
    }
    article p .location {
        font-family: arial;
        font-size: 1em;
        width: 36em;
    }
    article p label {
        font-family: arial;
        font-size: 1em;
        width: 12.5em;
    }
</style>

<h2>Planning</h2>

<div id='event_sources'><!-- event_sources placeholder --></div>

<script type='text/javascript'>
	"use strict";
	/*global $*/

    jQuery.get("./full_calendar.json", function(data) {

        var prop = {
            viewRender: function( view, element ) {
                var currDate = $("#event_sources").fullCalendar('getDate');
                var ajaxData = {
                    defaultView : view.name,
                    date : currDate.getDate(),
                    month : currDate.getMonth(),
                    year : currDate.getFullYear()
                };
                jQuery.ajax("./full_calendar", { method : "put", data : ajaxData });
            },
            dayClick: function(date, allDay, jsEvent, view) {
				var tz_offset = date.getTimezoneOffset(); // UTC offset
				date_end = date;
				var date_end = new Date(date);
				date_end.setHours(date.getHours() + 1);
				var data = {
				    tz_offset : tz_offset,
				    all_day : allDay,
				    event_start : date.toISOString(),
				    event_end : date_end.toISOString()
				};

                $('#confirm_dialog_content').load("./sources/events/new", data);

                $('#confirm_dialog').dialog({
                    width: 	600,
                    height: 370,
                    buttons: {
                        "Ajouter": function() {
                            $('#new_event_create_form').submit();
                        },
                        "Annuler": function() {
                            $(this).dialog("close");
                        }
                    },
                    title: "Ajouter un événement ici",
                    close: function() {
                        $('#event_sources').fullCalendar('gotoDate', date);
                    }
                }).dialog("open");

            },
        };

        $('#event_sources').fullCalendar($.extend(data, prop));

    });
</script>