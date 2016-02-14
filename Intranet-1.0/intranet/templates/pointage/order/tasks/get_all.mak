%if order and order.estimated_duration:
<!-- <% tasks_id = "tasks_{0}".format(order.uid) %> -->
<section id="${tasks_id}">
    <style type="text/css" scoped="scoped">
        .container-fluid {padding: 5px; width: 100%;}
        .row {display: block; clear: left;}
        .col-xs-1  {display: inline-block; vertical-align: middle; min-width:   3em; width:   8.33%; float: left; padding: 5px;}
        .col-xs-2  {display: inline-block; vertical-align: middle; min-width:   7em; width:  16.66%; float: left; padding: 5px;}
        .col-xs-4  {display: inline-block; vertical-align: middle; min-width:  14em; width:  33.00%; float: left; padding: 5px;}
        .col-xs-5  {display: inline-block; vertical-align: middle; min-width:  17em; width:  41.66%; float: left; padding: 5px;}
        .col-xs-6  {display: inline-block; vertical-align: middle; min-width:  21em; width:  50.00%; float: left; padding: 5px;}
        .col-xs-7  {display: inline-block; vertical-align: middle; min-width:  25em; width:  58.33%; float: left; padding: 5px;}
        .col-xs-10 {display: inline-block; vertical-align: middle; min-width:  35em; width:  83.33%; float: left; padding: 5px;}
        .col-xs-12 {display: inline-block; vertical-align: middle; min-width:  42em; width: 100.00%; float: left; padding: 5px;}
        #${tasks_id} footer nav  {float: left;}
    </style>

    <header>
        <h2>${title}</h2>
    </header>

    <div id="sortable" class="container-fluid">
    </div>

    <footer class="ui-state-default">
        <form id="new_task__form">
            <fieldset id="new_task" class="task ui-widget">
                <div class="row">
                    <div class="col-xs-12">
                        <nav>
                            <button type="submit" class="refresh_button" title="Met à jour la planificarion des tâches">Planifier tout</button>
                            <button type="submit" class="calendar_button" title="Afficher le planning des événements">Afficher le planning</button>
                        </nav>
                    </div>
                </div>
            </fieldset>
        </form>
    </footer>
</section>
<script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
%endif