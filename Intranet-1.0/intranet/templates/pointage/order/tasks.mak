<section>
    <style type="text/css" scoped="scoped">
        .container-fluid {padding: 5px; width: 100%;}
        .row-xs {display: block; clear: left;}
        .col-xs-1  {display: inline-block; vertical-align: middle; min-width:   3em; width:   8.33%; float: left; padding: 5px;}
        .col-xs-2  {display: inline-block; vertical-align: middle; min-width:   7em; width:  16.66%; float: left; padding: 5px;}
        .col-xs-4  {display: inline-block; vertical-align: middle; min-width:  14em; width:  33.00%; float: left; padding: 5px;}
        .col-xs-5  {display: inline-block; vertical-align: middle; min-width:  17em; width:  41.66%; float: left; padding: 5px;}
        .col-xs-6  {display: inline-block; vertical-align: middle; min-width:  21em; width:  50.00%; float: left; padding: 5px;}
        .col-xs-7  {display: inline-block; vertical-align: middle; min-width:  25em; width:  58.33%; float: left; padding: 5px;}
        .col-xs-10 {display: inline-block; vertical-align: middle; min-width:  35em; width:  83.33%; float: left; padding: 5px;}
        .col-xs-12 {display: inline-block; vertical-align: middle; min-width:  42em; width: 100.00%; float: left; padding: 5px;}

        fieldsets.task { border: none; }

        input.position          {text-align: right; font-weight: bold; width: 1.5em; }
        input.display_name      {text-align: left;  font-weight: bold; min-width: 18em;}
        label.prev_uid          {text-align: right}
        select.prev_uid         {text-align: left;}

        label.description       {display: block;}
        textarea.description    {width: 100%;}
        table.charge            {margin: 0 auto 0 auto;}
        table.charge th         {font-size: .8em;}
        table.charge input[type="number"] {text-align: right;}
        div.status              {font-size: .8em;}

        label.assignment {display: block; text-align: right; margin: 2em 0 2em 0;}
        div.assignment {
        display: block;
        background-color: #fff;
        -moz-border-radius: 5px;
        -webkit-border-radius: 5px;
        border-radius: 5px;
        border: solid 1px #000;
        padding: 2px;
        }
        span.badge {
        display: inline-block;
        padding: 5px;
        height: 4.5em;
        vertical-align: middle;
        }
        span.badge table.planning       {margin: auto 0 auto 0; border: none;}
        span.badge table.planning tr    {font-size: .8em}
        span.badge table.planning td    {padding: 0px;}
        span.badge input[type="number"]     {text-align: right; width:  4em;}
        span.badge input[type="date"]       {text-align: left;  width: 10em;}
        span.badge select.add   {margin-top: 1.2em; width: 8em;}

        article nav  {float: right;}
        footer  nav  {float: left;}
    </style>

    <header>
        <h2>Liste des tâches</h2>
    </header>

    <div id="sortable" class="container-fluid">
        <article class="ui-state-default">
            <form id="task_1__form">
                <fieldset id="task_1" class="task ui-widget">
                    <div class="row-xs">
                        <div class="col-xs-6">
                            <input class="position" name="position" value="1" disabled="disabled"/>
                            <input class="display_name" name="display_name" value="Étude / commercialisation" title="Nom de la tâche"/>
                        </div>
                        <div class="col-xs-6">
                            <label class="prev_uid" for="task_1__prev_uid">Prédécesseur&nbsp;:</label>
                            <select class="prev_uid ui-widget ui-state-default ui-corner-all" id="task_1__prev_uid" name="prev_uid" title="Sélectionnez un prédécesseur (ou aucun)">
                                <option value="" selected="selected">&lt;aucun prédécesseur&gt;</option>
                                <option value="2">Fabrication</option>
                                <option value="3">Finition</option>
                                <option value="4">Divers</option>
                            </select>
                        </div>
                    </div>
                    <div class="row-xs">
                        <div class="col-xs-6">
                            <label class="description" for="task_1__description">Description&nbsp;:</label>
                        <textarea class="description" id="task_1__description" name="description" title="Description de la tâche à effectuer"
                                  rows="3" cols="30">Devis lit enfant</textarea>
                        </div>
                        <div class="col-xs-6">
                            <table class="charge">
                                <thead>
                                <tr>
                                    <th></th>
                                    <th>Effectuée</th>
                                    <th>Restante</th>
                                    <th>Totale</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <th>Charge&nbsp;:</th>
                                    <td>
                                        <input name="done_duration" type="number" value="16"
                                               disabled="disabled"
                                               min="0" max="999" step=".25" placeholder="(heures)"
                                               title="Durée déjà effectuée et pointée"/>
                                    </td>
                                    <td>
                                        <input name="remain_duration" type="number" value="0"
                                               min="0" max="999" step=".25" placeholder="(heures)"
                                               title="Durée restante estimée"/>
                                    </td>
                                    <td>
                                        <input name="total_duration" type="number" value="16"
                                               disabled="disabled"
                                               min="0" max="999" step=".25" placeholder="(heures)"
                                               title="Durée totale effectuée + estimée"/>
                                    </td>
                                </tr>
                                <tr>
                                    <th>Statut&nbsp;:</th>
                                    <td colspan="3">
                                        <div class="status">
                                            <input type="radio" id="task_1__status1" name="status"/>
                                            <label for="task_1__status1">Attente</label>
                                            <input type="radio" id="task_1__status2" name="status"/>
                                            <label for="task_1__status2">En cours</label>
                                            <input type="radio" id="task_1__status3" name="status" checked="checked"/>
                                            <label for="task_1__status3">Terminé</label>
                                        </div>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="row-xs">
                        <div class="col-xs-2">
                            <label class="assignment">Affectation(s)&nbsp;:</label>
                        </div>
                        <div class="col-xs-10">
                            <div class="assignment">
                            <span class="badge ui-widget ui-state-default ui-corner-all">
                                <table class="planning">
                                    <tbody>
                                    <tr>
                                        <td rowspan="2"><img class="valignMiddle picture_box_inner_min" alt="POUTEAU Nicolas - Photo" src="/photo/pointage/employee/employee_3_1380980369.67.jpg"></td>
                                        <td><label>taux&nbsp;: </label><input type="number" value="80" name="percent" min="1" max="100" step="1"><span>%</span></td>
                                        <td><button type="submit" class="delete_button_icon" title="Supprimer l‘affectation">-</button></td>
                                    </tr>
                                    <tr>
                                        <td><label>le&nbsp;: </label><input type="date" value="" name="event"/></td>
                                        <td><button type="submit" class="refresh_button_icon" title="Planifier l‘affectation">#</button></td>
                                    </tr>
                                    </tbody>
                                </table>
                            </span>
                            <span class="badge ui-widget ui-state-default ui-corner-all">
                                <select name="employee_uid" class="add ui-widget ui-state-default ui-corner-all" title="Liste des employés">
                                    <option value="" selected="selected">&lt;Ajouter&gt;</option>
                                    <option value="6">CLERET Thierry</option>
                                    <option value="4">LANOE Fabrice</option>
                                    <option value="1">LEVEQUE Bernard</option>
                                    <option value="8">MAIGNAN Nicolas</option>
                                    <option value="9">MERCIER Marius</option>
                                    <option value="3">MOUSSAY Damien</option>
                                    <option value="5">POUTEAU Nicolas</option>
                                    <option value="2">RIDEREAU Charlie</option>
                                </select>
                            </span>
                            </div>
                        </div>
                    </div>
                    <div class="row-xs">
                        <div class="col-xs-12">
                            <nav>
                                <button type="submit" class="refresh_button" title="Met à jour la planification de la tâche">Planifier</button>
                                <button type="submit" class="update_button" title="Modifier la tâche">Modifier</button>
                                <button type="submit" class="delete_button" title="Supprimer la tâche">Supprimer</button>
                            </nav>
                        </div>
                    </div>
                </fieldset>
            </form>
        </article>
        <article class="ui-state-default">
            <form id="task_2__form">
                <fieldset id="task_2" class="task ui-widget">
                    <div class="row-xs">
                        <div class="col-xs-6">
                            <input class="position" name="position" value="2" disabled="disabled"/>
                            <input class="display_name" name="display_name" value="Fabrication" title="Nom de la tâche"/>
                        </div>
                        <div class="col-xs-6">
                            <label class="prev_uid" for="task_2__prev_uid">Prédécesseur&nbsp;:</label>
                            <select class="prev_uid ui-widget ui-state-default ui-corner-all" id="task_2__prev_uid" name="prev_uid" title="Sélectionnez un prédécesseur (ou aucun)">
                                <option value="">&lt;aucun prédécesseur&gt;</option>
                                <option value="1" selected="selected">Étude / commercialisation</option>
                                <option value="3">Finition</option>
                                <option value="4">Divers</option>
                            </select>
                        </div>
                    </div>
                    <div class="row-xs">
                        <div class="col-xs-6">
                            <label class="description" for="task_2__description">Description&nbsp;:</label>
                        <textarea class="description" id="task_2__description" name="description" title="Description de la tâche à effectuer"
                                  rows="3" cols="30">Usiner les pièces du lit et les monter.</textarea>
                        </div>
                        <div class="col-xs-6">
                            <table class="charge">
                                <thead>
                                <tr>
                                    <th></th>
                                    <th>Effectuée</th>
                                    <th>Restante</th>
                                    <th>Totale</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr>
                                    <th>Charge&nbsp;:</th>
                                    <td>
                                        <input name="done_duration" type="number" value="14.5"
                                               disabled="disabled"
                                               min="0" max="999" step=".25" placeholder="(heures)"
                                               title="Durée déjà effectuée et pointée"/>
                                    </td>
                                    <td>
                                        <input name="remain_duration" type="number" value="27.5"
                                               min="0" max="999" step=".25" placeholder="(heures)"
                                               title="Durée restante estimée"/>
                                    </td>
                                    <td>
                                        <input name="total_duration" type="number" value="41.0"
                                               disabled="disabled"
                                               min="0" max="999" step=".25" placeholder="(heures)"
                                               title="Durée totale effectuée + estimée"/>
                                    </td>
                                </tr>
                                <tr>
                                    <th>Statut&nbsp;:</th>
                                    <td colspan="3">
                                        <div class="status">
                                            <input type="radio" id="task_2__status1" name="status"/>
                                            <label for="task_2__status1">Attente</label>
                                            <input type="radio" id="task_2__status2" name="status" checked="checked"/>
                                            <label for="task_2__status2">En cours</label>
                                            <input type="radio" id="task_2__status3" name="status"/>
                                            <label for="task_2__status3">Terminé</label>
                                        </div>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="row-xs">
                        <div class="col-xs-2">
                            <label class="assignment">Affectation(s)&nbsp;:</label>
                        </div>
                        <div class="col-xs-10">
                            <div class="assignment">
                            <span class="badge ui-widget ui-state-default ui-corner-all">
                                <table class="planning">
                                    <tbody>
                                    <tr>
                                        <td rowspan="2"><img class="valignMiddle picture_box_inner_min" alt="LEVEQUE Bernard - Photo" src="/photo/pointage/employee/employee_2_1380980350.28.jpg"></td>
                                        <td><label>taux&nbsp;: </label><input type="number" value="20" name="percent" min="1" max="100" step="1"><span>%</span></td>
                                        <td><button type="submit" class="delete_button_icon" title="Supprimer l‘affectation">-</button></td>
                                    </tr>
                                    <tr>
                                        <td><label>le&nbsp;: </label><input type="date" value="2015-06-15" name="event"/></td>
                                        <td><button type="submit" class="refresh_button_icon" title="Planifier l‘affectation">#</button></td>
                                    </tr>
                                    </tbody>
                                </table>
                            </span>
                            <span class="badge ui-widget ui-state-default ui-corner-all">
                                <table class="planning">
                                    <tbody>
                                    <tr>
                                        <td rowspan="2"><img class="valignMiddle picture_box_inner_min" alt="LANOE Fabrice - Photo" src="/photo/pointage/employee/employee_7_1380980436.08.jpg"></td>
                                        <td><label>taux&nbsp;: </label><input type="number" value="100" name="percent" min="1" max="100" step="1"><span>%</span></td>
                                        <td><button type="submit" class="delete_button_icon" title="Supprimer l‘affectation">-</button></td>
                                    </tr>
                                    <tr>
                                        <td><label>le&nbsp;: </label><input type="date" name="event"/></td>
                                        <td><button type="submit" class="refresh_button_icon" title="Planifier l‘affectation">#</button></td>
                                    </tr>
                                    </tbody>
                                </table>
                            </span>
                            <span class="badge ui-widget ui-state-default ui-corner-all">
                                <select name="employee_uid" class="add ui-widget ui-state-default ui-corner-all" title="Liste des employés">
                                    <option value="" selected="selected">&lt;Ajouter&gt;</option>
                                    <option value="6">CLERET Thierry</option>
                                    <option value="4">LANOE Fabrice</option>
                                    <option value="1">LEVEQUE Bernard</option>
                                    <option value="8">MAIGNAN Nicolas</option>
                                    <option value="9">MERCIER Marius</option>
                                    <option value="3">MOUSSAY Damien</option>
                                    <option value="5">POUTEAU Nicolas</option>
                                    <option value="2">RIDEREAU Charlie</option>
                                </select>
                            </span>
                            </div>
                        </div>
                    </div>
                    <div class="row-xs">
                        <div class="col-xs-12">
                            <nav>
                                <button type="submit" class="refresh_button" title="Met à jour la planification de la tâche">Planifier</button>
                                <button type="submit" class="update_button" title="Modifier la tâche">Modifier</button>
                                <button type="submit" class="delete_button" title="Supprimer la tâche">Supprimer</button>
                            </nav>
                        </div>
                    </div>
                </fieldset>
            </form>
        </article>
        <article class="ui-state-default">
            <form id="task_3__form">
                <fieldset id="task_3" class="task ui-widget">
                    <div class="row-xs">
                        <div class="col-xs-6">
                            <input class="position" name="position" value="3" disabled="disabled"/>
                            <input class="display_name" name="display_name" value="Finition" title="Nom de la tâche"/>
                        </div>
                        <div class="col-xs-6">
                            <label class="prev_uid" for="task_3__prev_uid">Prédécesseur&nbsp;:</label>
                            <select class="prev_uid ui-widget ui-state-default ui-corner-all" id="task_3__prev_uid" name="prev_uid" title="Sélectionnez un prédécesseur (ou aucun)">
                                <option value="">&lt;aucun prédécesseur&gt;</option>
                                <option value="1">Étude / commercialisation</option>
                                <option value="2" selected="selected">Fabrication</option>
                                <option value="4">Divers</option>
                            </select>
                        </div>
                    </div>
                    <div class="row-xs">
                        <div class="col-xs-6">
                            <label class="description" for="task_3__description">Description&nbsp;:</label>
                        <textarea class="description" id="task_3__description" name="description" title="Description de la tâche à effectuer"
                                  rows="3" cols="30">Peinture lavande.</textarea>
                        </div>
                        <div class="col-xs-6">
                            <table class="charge">
                                <thead>
                                <tr>
                                    <th></th>
                                    <th>Effectuée</th>
                                    <th>Restante</th>
                                    <th>Totale</th>
                                </tr>

                                </thead>
                                <tbody>
                                <tr>
                                    <th>Charge&nbsp;:</th>
                                    <td>
                                        <input name="done_duration" type="number" value="0"
                                               disabled="disabled"
                                               min="0" max="999" step=".25" placeholder="(heures)"
                                               title="Durée déjà effectuée et pointée"/>
                                    </td>
                                    <td>
                                        <input name="remain_duration" type="number" value=""
                                               min="0" max="999" step=".25" placeholder="(heures)"
                                               title="Durée restante estimée"/>
                                    </td>
                                    <td>
                                        <input name="total_duration" type="number" value=""
                                               disabled="disabled"
                                               min="0" max="999" step=".25" placeholder="(heures)"
                                               title="Durée totale effectuée + estimée"/>
                                    </td>
                                </tr>
                                <tr>
                                    <th>Statut&nbsp;:</th>
                                    <td colspan="3">
                                        <div class="status">
                                            <input type="radio" id="task_3__status1" name="status" checked="checked"/>
                                            <label for="task_3__status1">Attente</label>
                                            <input type="radio" id="task_3__status2" name="status"/>
                                            <label for="task_3__status2">En cours</label>
                                            <input type="radio" id="task_3__status3" name="status"/>
                                            <label for="task_3__status3">Terminé</label>
                                        </div>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="row-xs">
                        <div class="col-xs-2">
                            <label class="assignment">Affectation(s)&nbsp;:</label>
                        </div>
                        <div class="col-xs-10">
                            <div class="assignment">
                            <span class="badge ui-widget ui-state-default ui-corner-all">
                                <select name="employee_uid" class="add ui-widget ui-state-default ui-corner-all" title="Liste des employés">
                                    <option value="" selected="selected">&lt;Ajouter&gt;</option>
                                    <option value="6">CLERET Thierry</option>
                                    <option value="4">LANOE Fabrice</option>
                                    <option value="1">LEVEQUE Bernard</option>
                                    <option value="8">MAIGNAN Nicolas</option>
                                    <option value="9">MERCIER Marius</option>
                                    <option value="3">MOUSSAY Damien</option>
                                    <option value="5">POUTEAU Nicolas</option>
                                    <option value="2">RIDEREAU Charlie</option>
                                </select>
                            </span>
                            </div>
                        </div>
                    </div>
                    <div class="row-xs">
                        <div class="col-xs-12">
                            <nav>
                                <button type="submit" class="refresh_button" title="Met à jour la planification de la tâche">Planifier</button>
                                <button type="submit" class="update_button"  title="Modifier la tâche">Modifier</button>
                                <button type="submit" class="delete_button"  title="Supprimer la tâche">Supprimer</button>
                            </nav>
                        </div>
                    </div>
                </fieldset>
            </form>
        </article>
    </div>

    <footer class="ui-state-default">
        <form id="new_task__form">
            <fieldset id="new_task" class="task ui-widget">
                <div class="row-xs">
                    <div class="col-xs-12">
                        <nav>
                            <button type="submit" class="refresh_button" title="Met à jour la planification des tâches">Planifier tout</button>
                            <button type="submit" class="new_button" title="Ajouter une nouvelle tâche">Ajouter une tâche</button>
                            <button type="submit" class="calendar_button" title="Afficher le planning des événements">Afficher le planning</button>
                        </nav>
                    </div>
                </div>
            </fieldset>
        </form>
    </footer>
</section>

<script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
<script type="text/javascript">
  $(function() {
    $("#sortable").sortable();
    $("#sortable").disableSelection();
    $(".status").buttonset();
  });
</script>
