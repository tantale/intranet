<%namespace file="intranet.templates.pointage.order.tasks.task_widget" import="task_form"/>
%if order and order.estimated_duration:
<% tasks_id = "tasks_{0}".format(order.uid) %>
<section id="${tasks_id}">
    <style type="text/css" scoped="scoped">
        #${tasks_id} article nav  {float: right;}
        #${tasks_id} footer nav {float: left;}

        #${tasks_id} fieldsets.task { border: none; }

        #${tasks_id} input.position          {text-align: right; font-weight: bold; width: 1.5em; }
        #${tasks_id} input.label             {text-align: left;  font-weight: bold; min-width: 18em;}
        #${tasks_id} label.prev_uid          {text-align: right}
        #${tasks_id} select.prev_uid         {text-align: left;}

        #${tasks_id} label.description       {display: block;}
        #${tasks_id} textarea.description    {width: 100%;}
        #${tasks_id} table.charge            {margin: 0 auto 0 auto;}
        #${tasks_id} table.charge th         {font-size: .8em;}
        #${tasks_id} table.charge input[type="number"] {text-align: right;}
        #${tasks_id} div.status              {font-size: .8em;}
        #${tasks_id} label.assignment {display: block; text-align: right; margin: 2em 0 2em 0;}
        #${tasks_id} div.assignment {
            display: block;
            background-color: #fff;
            -moz-border-radius: 5px;
            -webkit-border-radius: 5px;
            border-radius: 5px;
            border: solid 1px #000;
            padding: 2px;
        }
        #${tasks_id} div.badge {
            display: inline-block;
            padding: 5px;
            height: 4.5em;
            vertical-align: middle;
        }
        #${tasks_id} div.badge table.planning       {margin: auto 0 auto 0; border: none;}
        #${tasks_id} div.badge table.planning tr    {font-size: .8em}
        #${tasks_id} div.badge table.planning td    {padding: 0px;}
        #${tasks_id} div.badge input[type="number"]     {text-align: right; width:  4em;}
        #${tasks_id} div.badge input[type="date"]       {text-align: left;  width: 10em;}
        #${tasks_id} div.badge select.add   {margin-top: 1.2em; width: 8em;}
    </style>

    <header>
        <h2>${title}</h2>
    </header>
    <div class="container-fluid">
        %for task in order.order_phase_list:
        <% task_id = "task_{0}".format(task.uid) %>
        <article id="${task_id}" class="ui-state-default">${task_form(task, active_employees)}</article>
        %endfor
    </div>
    <footer class="ui-state-default">
        <form id="new_task__form">
            <fieldset id="new_task" class="task ui-widget">
                <div class="row-xs">
                    <div class="col-xs-12">
                        <nav>
                            <button type="submit" class="refresh_button"
                                    title="Met à jour la planificarion des tâches">Planifier tout
                            </button>
                            <button type="submit" class="calendar_button"
                                    title="Afficher le planning des événements">Afficher le planning
                            </button>
                        </nav>
                    </div>
                </div>
            </fieldset>
        </form>
    </footer>
</section>
<script type="application/javascript" defer="defer">
    $(function() {
        $("#${tasks_id} .refresh_button").button({
            text : true,
            icons : {
                primary : "ui-icon-refresh"
            }
        });
        $("#${tasks_id} .calendar_button").button({
            text : true,
            icons : {
                primary : "ui-icon-calendar"
            }
        });
    });
</script>
%endif