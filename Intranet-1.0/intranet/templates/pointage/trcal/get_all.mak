# -*- coding: utf-8 -*-
## cal_start=cal_start,
## cal_end=cal_end,
## cal_curr=cal_curr,
## employee=employee
<%! import json %>
<div id='caltoolbar'><!-- toolbar placeholder --></div>
<div id='calendar'><!-- calendar placeholder --></div>
<%
events_url = tg.url('./events', dict(employee_uid=employee.uid))
events_url_json = json.dumps(events_url)

new_url = tg.url('./new', dict(employee_uid=employee.uid))
new_url_json = json.dumps(new_url)

edit_url = tg.url('./edit')
edit_url_json = json.dumps(edit_url)

event_drop_url = tg.url('./event_drop')
event_drop_url_json = json.dumps(event_drop_url)

event_resize_url = tg.url('./event_resize')
event_resize_url_json = json.dumps(event_resize_url)

## cal_curr_json = json.dumps(cal_curr)
%>\
<script type='text/javascript'>
    "use strict";
    /*global $*/
    function load_order_list(cal_start, cal_end) {
        if (!cal_start || !cal_end) {
            var cal_curr = new Date(), y = cal_curr.getFullYear(), m = cal_curr.getMonth();
            cal_start = new Date(y, m, 1);
            cal_end = new Date(y, m + 1, 1);
        }
        $('#order_get_all input[name=cal_start]').val(cal_start.getTime() / 1000);
        $('#order_get_all input[name=cal_end]').val(cal_end.getTime() / 1000);
        $('#order_get_all').submit();
    }

    function load_employee_list(cal_start, cal_end, cal_curr) {
        if (!cal_start || !cal_end || !cal_curr) {
            cal_curr = new Date(), y = cal_curr.getFullYear(), m = cal_curr.getMonth();
            cal_start = new Date(y, m, 1);
            cal_end = new Date(y, m + 1, 1);
        }
        $('#caltoolbar').load("./employee_get_all", {
            'cal_start': cal_start.getTime() / 1000,
            'cal_end': cal_end.getTime() / 1000,
            'cal_curr': Math.round(cal_curr.getTime() / 1000),
            'employee_uid' : ${employee.uid}
            });
    }

    function on_events_load(start_date, end_date, callback) {
        var curr_date = $('#calendar').fullCalendar('getDate');
        $.ajax({
            url: ${events_url_json|n},
            dataType: 'json',
            data: {
                start: Math.round(start_date.getTime() / 1000),
                end: Math.round(end_date.getTime() / 1000)
            },
            success: function(events) {
                callback(events);
                load_order_list(start_date, end_date);
                load_employee_list(start_date, end_date, curr_date);
            },
            error: function() {
                callback();
                var title = "Erreur de connexion HTTP",
                    text = "Impossible de récupérer les événements\u00a0!";
                displayErrDialog(title, text);
            }
        });
    }

    function on_event_render(event, element, view) {
        var start_date = $.fullCalendar.parseDate(event.start),
            end_date = $.fullCalendar.parseDate(event.end),
            event_duration = (end_date - start_date) / 3600.0 / 1000,
            duration = event_duration.toString().replace('.', ',')
        element.attr('title', event.comment).find('.fc-event-time')
            .text(duration).css('padding-left: .5em;');
    }

    function on_event_drop(event, dayDelta, minuteDelta, allDay, revertFunc, jsEvent, ui, view) {
        if (allDay) {
            console.info("Please, this event ins't a all day event!");
            revertFunc();
        } else {
            $.ajax({
                type: "GET",
                url: ${event_drop_url_json|n},
                data: {
                    // id = 'cal_event_###'
                    uid: event.id.split('_')[2],
                    day_delta: dayDelta,
                    minute_delta: minuteDelta
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
        }
    }

    function on_event_resize(event, dayDelta, minuteDelta, revertFunc, jsEvent, ui, view) {
        $.ajax({
            type: "GET",
            url: ${event_resize_url_json|n},
            data: {
                // id = 'cal_event_###'
                uid: event.id.split('_')[2],
                day_delta: dayDelta,
                minute_delta: minuteDelta
            },
            success: function(){
                console.info("Event duration succefully updated.");
                console.info("gotoDate: " + event.start.toISOString());
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
    }

    function open_new_event_dialog(event_td, date, allDay) {
        var selected = $('ul.selectable .ui-selected');
        if (selected.length) {
            console.debug('------- open_new_event_dialog');
            var url = ${new_url_json|n}, // contains: employee_uid
                tz_offset = date.getTimezoneOffset(), // UTC offset
                order_phase_uid =  selected.attr('id').split('_')[3];
            console.debug('------- tz_offset: ' + tz_offset.toString());

            url += "&order_phase_uid=" + order_phase_uid;
            url += "&date=" + date.toISOString();
            url += "&allDay=" + allDay;
            url += "&tz_offset=" + tz_offset.toString();

            $('#confirm_dialog_content').load(url);
            $('#confirm_dialog').dialog({
                width: 	540,
                height: 370,
                buttons: {
                    "Ajouter": function() {
                        $('#cal_event_create').submit();
                    },
                    "Annuler": function() {
                        $(this).dialog("close");
                    }
                },
                title: "Saisir un pointage",
                close: function() {
                    console.info('gotoDate: '+ date.toISOString());
                    $('#calendar').fullCalendar('gotoDate', date);
                    console.debug('------- /open_new_event_dialog');
                }
            }).dialog("open");
        } else {
            var msg = $('<div id="flash"></div>')
                .append($('<div class="error"/>')
                        .text("Veuillez sélectionner une phase dans la liste des commandes\u00a0!"));
            $('#confirm_dialog_content').empty().append(msg);
            $('#confirm_dialog').dialog({
                width: 	400,
                height: 200,
                buttons: {
                    "OK": function() {
                        $(this).dialog("close");
                    }
                },
                title: "Aucune phase sélectionnée",
                close: function() {
                    console.info('gotoDate: '+ date.toISOString());
                    $('#calendar').fullCalendar('gotoDate', date);
                }
            }).dialog("open");
        }
    }

    function open_edit_event_dialog(event_div, event, view) {
        // 'this' is set to the event's <div> element.
        var uid = event.id.split('_')[2], // id = 'cal_event_###'
            tz_offset = event.start.getTimezoneOffset(),
            url = ${edit_url_json|n} + "?uid=" + uid;
            url += "&tz_offset=" + tz_offset;
        $('#confirm_dialog_content').load(url);
        $('#confirm_dialog').dialog({
            width: 	540,
            height: 370,
            buttons: {
                "Modifier": function() {
                    $('#cal_event_update').submit();
                },
                "Supprimer": function() {
                    $('#cal_event_delete').submit();
                },
                "Annuler": function() {
                    $(this).dialog("close");
                }
            },
            title: "Modifier un pointage",
            close: function() {
                console.info('gotoDate: '+ event.start.toISOString());
                $('#calendar').fullCalendar('gotoDate', event.start);
            }
        }).dialog("open");
    }

    function displayErrDialog(title, text) {
        var msg = $('<div id="flash"></div>') //
            .append($('<div class="error"/>').text(text));
        $('#confirm_dialog_content').empty().append(msg);
        $('#confirm_dialog').dialog({
            width: 	400,
            height: 200,
            buttons: {
                "OK": function() {
                    $(this).dialog("close");
                }
            },
            title: title
        }).dialog("open");
    }

    jQuery.get("./full_calendar.json", function(data){

        var prop = {
            viewRender: function( view, element ) {
                var currDate = $("#calendar").fullCalendar('getDate');
                var ajaxData = {
                    defaultView : view.name,
                    date : currDate.getDate(),
                    month : currDate.getMonth(),
                    year : currDate.getFullYear()
                };
                jQuery.ajax("./full_calendar", { method : "put", data : ajaxData });
            },
            // Only accept <li/> elements
            droppable: true,
            dropAccept: "li",
            drop: function(date, allDay) {
                open_new_event_dialog(this, date, allDay);
            },
            eventDrop: on_event_drop,
            dayClick: function(date, allDay, jsEvent, view) {
                open_new_event_dialog(this, date, allDay);
            },
            eventClick: function(event, jsEvent, view) {
                open_edit_event_dialog(this, event, view);
            },
            eventResize: on_event_resize,
            eventSources: [{
                // http://arshaw.com/fullcalendar/docs/event_data/events_function/
                events: on_events_load
                }],
            eventRender : on_event_render
        };

        $('#calendar').fullCalendar($.extend(data, prop));
    });
</script>
