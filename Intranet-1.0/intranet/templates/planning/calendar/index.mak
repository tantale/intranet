<div>
    <h2>Liste des calendriers</h2>
    <table id="calendar" cellpadding="0" cellspacing="2" border="0"
           class="record-table"
           style="page-break-inside: avoid">
        <thead>
        <tr>
            <th class="record-table-name">${_(u"Libellé")}</th>
            <th class="record-table-label">${_(u"Description")}</th>
            <th class="record-table-name">${_(u"Employé")}</th>
            <th class="record-table-name">${_(u"Horaires")}</th>
            <th><!--empty--></th>
        </tr>
        </thead>
        <tbody></tbody>
        <tfoot></tfoot>
    </table>
    <script type='text/javascript'>
    $(function() {
        $("#calendar").styleTable();
        $('#calendar tbody').load("${tg.url('/admin/planning/calendar/get_all')}");
        $('#calendar tfoot').load("${tg.url('/admin/planning/calendar/new')}");
    });
    </script>
</div>
