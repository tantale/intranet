<%def name="charge_table(order)">
<table class="charge">
    <thead>
    <tr>
        <th></th>
        <th>Estimée</th>
        <th>Effectuée</th>
        <th>Restante</th>
        <th>Totale</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <th>Charge&nbsp;:</th>
        <td>
            <input class="change"
                   name="estimated_duration" type="number" value="${order.estimated_duration}"
                   readonly="readonly"
                   min="0" max="999" step=".25" placeholder="(heures)"
                   title="Durée estimée à partir des statistiques"/>
        </td>
        <td>
            <input class="change"
                   name="tracked_duration" type="number" value="${order.tracked_duration}"
                   readonly="readonly"
                   min="0" max="999" step=".25" placeholder="(heures)"
                   title="Durée déjà effectuée et pointée"/>
        </td>
        <td>
            <input class="change"
                   name="remain_duration" type="number" value="${order.remain_duration}"
                   readonly="readonly"
                   min="0" max="999" step=".25" placeholder="(heures)"
                   title="Durée restante estimée"/>
        </td>
        <td>
            <input class="change"
                   name="total_duration" type="number" value="${order.total_duration}"
                   readonly="readonly"
                   min="0" max="999" step=".25" placeholder="(heures)"
                   title="Durée totale : effectuée + restante"/>
        </td>
    </tr>
    <tr>
        <th>Statut&nbsp;:</th>
        <td colspan="4">
            <div class="task_status">
                %for status_info in order.all_status_info:
                %if status_info['checked']:
                <label title="${status_info['description']}"><input class="change"
                                                                    disabled="disabled"
                                                                    type="radio" checked="checked"
                                                                    value="${status_info['value']}"
                                                                    name="task_status"/>${status_info['label']}</label>
                %else:
                <label title="${status_info['description']}"><input class="change"
                                                                    disabled="disabled"
                                                                    type="radio"
                                                                    value="${status_info['value']}"
                                                                    name="task_status"/>${status_info['label']}</label>
                %endif
                %endfor
            </div>
        </td>
    </tr>
    </tbody>
</table>
</%def>

