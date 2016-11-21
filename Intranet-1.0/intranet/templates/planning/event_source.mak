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
        width: 19em;
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

    function displayErrDialog(title, text) {
        var msg = $('<div id="flash"></div>') //
            .append($('<div class="error"/>').text(text));
        $('#confirm_dialog_content').empty().append(msg);
        $('#confirm_dialog').dialog({
            width:  400,
            height: 200,
            buttons: {
                "OK": function() {
                    $(this).dialog("close");
                }
            },
            title: title
        }).dialog("open");
    }

    jQuery.get("./full_calendar.json", function(data) {

        var prop = {
            eventSources: ${ eventSources |n},
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
                var tz_offset = date.getTimezoneOffset();  // UTC offset
                var date_end = new Date(date);
                var firstHour = view.calendar.options.firstHour;
                console.log(firstHour);

                // Set allDay to false when view is Month
                if (view.name == "month") {
                    allDay = false;
                    date.setHours(firstHour);
                }

                if (!allDay) {
                    date_end.setHours(date.getHours() + 1);
                }

                // Create a URL to use "GET" (instead of "POST")
                var url = "./sources/events/new?";
                url += "tz_offset=" + encodeURIComponent(tz_offset) + "&";
                url += "all_day=" + encodeURIComponent(allDay) + "&";
                url += "event_start=" + encodeURIComponent(date.toISOString()) + "&";
                url += "event_end=" + encodeURIComponent(date_end.toISOString()) + "&";
                
                $('#confirm_dialog_content').load(url, function(){
                    $('#confirm_dialog').dialog({
                        width:  600,
                        height: 450,
                        buttons: {
                            "Ajouter": function() {
                                $('#event_new_form').submit();
                            },
                            "Annuler": function() {
                                $(this).dialog("close");
                            }
                        },
                        title: "Ajouter un événement",
                        close: function() {
                            $('#event_sources').fullCalendar('gotoDate', date);
                        }
                    }).dialog("open");
                });
            },
            eventClick: function(event, jsEvent, view) {
                var tz_offset = event.start.getTimezoneOffset();  // UTC offset
                var uid = event.id.split("_")[2];

                // Create a URL to use "GET" (instead of "POST")
                var url = "./sources/" + event.calendar_uid + "/events/" + uid + "/edit?";
                url += "tz_offset=" + encodeURIComponent(tz_offset);

                $('#confirm_dialog_content').load(url, function(){
                    $('#confirm_dialog').dialog({
                        width:  600,
                        height: 450,
                        buttons: {
                            "Modifier": function() {
                                $('#event_edit_form').submit();
                            },
                            "Supprimer": function() {
                                $('#event_delete_form').submit();
                            },
                            "Annuler": function() {
                                $(this).dialog("close");
                            }
                        },
                        title: "Modifier/Supprimer un événement",
                        close: function() {
                            $('#event_sources').fullCalendar('gotoDate', event.start);
                        }
                    }).dialog("open");  
                });
            },
            eventDrop: function(event, dayDelta, minuteDelta, allDay, revertFunc) {
                var
                    uid = event.id.split("_")[2],
                    url = "./sources/" + event.calendar_uid + "/events/" + uid + "/event_drop";

                $.ajax({
                    type: "GET",
                    url: url,
                    data: {
                        day_delta: dayDelta,
                        minute_delta: minuteDelta,
                        all_day: allDay
                    },
                    success: function(){
                        $('#calendar').fullCalendar('gotoDate', event.start);
                    },
                    error: function() {
                        revertFunc();
                        var title = "Erreur de connexion HTTP",
                            text = "Impossible de mettre à jour l\u2019événement\u00a0!";
                        displayErrDialog(title, text);
                    }
                });
            },
            eventResize: function(event, dayDelta, minuteDelta, revertFunc) {
                var
                    uid = event.id.split("_")[2],
                    url = "./sources/" + event.calendar_uid + "/events/" + uid + "/event_resize";

                $.ajax({
                    type: "GET",
                    url: url,
                    data: {
                        day_delta: dayDelta,
                        minute_delta: minuteDelta
                    },
                    success: function(){
                        $('#calendar').fullCalendar('gotoDate', event.start);
                        if (dayDelta) {
                            $('#calendar').fullCalendar('refetchEvents');
                        }
                    },
                    error: function() {
                        revertFunc();
                        var title = "Erreur de connexion HTTP",
                            text = "Impossible de mettre à jour la durée de l\u2019événements\u00a0!";
                        displayErrDialog(title, text);
                    }
                });
            },
            eventRender: function(event, element, view) {
                var start_date = $.fullCalendar.parseDate(event.start),
                    end_date = $.fullCalendar.parseDate(event.end),
                    event_duration = (end_date - start_date) / 3600.0 / 1000,
                    duration = event_duration.toString().replace('.', ',')
                var eventTime = element.find('.fc-event-time');
                var hour = eventTime.text();
                if (hour.indexOf(':') == -1) {
                    // append ":00" to the hour (missing)
                    hour = hour + ":00";
                }
                eventTime.text(hour + " (" + duration + "\u00a0h)")
                    .css({display: 'inline-block'});

                // Add the *description* to the event title (for tooltip).
                element.attr('title', event.description);

                if (event.label) {
                    var eventInner = element.find('.fc-event-inner');
                    var label = $('<span/>')
                        .css({display: 'inline-block', padding: '3px'})
                        .addClass('colorFrame')
                        .addClass(event.project_cat).append(event.label);
                    label.appendTo(eventInner);
                }
            }
        };

        $('#event_sources').fullCalendar($.extend(data, prop));

    });

</script>