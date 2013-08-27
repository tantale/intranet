# -*- coding: utf-8 -*-
<%doc>
:template: intranet.templates.pointage.order.get_one
:date: 2013-08-11
:author: Laurent LAPORTE <sandlol2009@gmail.com>
</%doc>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
%if flash:
    ${flash | n}
%endif
<h3>Détail de la commande</h3>
<table>
<tbody>
<tr>
<th>Référence</th>
<td>${order.order_ref}</td>
</tr>
<tr>
<th>Catégorie</th>
<td class='${order.project_cat}'>${order_cat_label}</td>
</tr>
<tr>
<th>Date de création</th>
<td>${order.creation_date}</td>
</tr>
<tr>
<th>Date de clôture</th>
<td>${order.close_date}</td>
</tr>
</tbody>
</table>

<h3>Liste des phases</h3>
%if order_phase_list:
<table>
<thead>
<tr>
<th>Position</th>
<th>Libellé</th>
</tr>
</thead>
<tbody>
%for order_phase in order_phase_list:
<tr>
<td>${order_phase.position}</td>
<td>${order_phase.label}</td>
</tr>
%endfor
</tbody>
</table>
%else:
<p><strong>Cette commande ne possède pas de phase</strong></p>
%endif
