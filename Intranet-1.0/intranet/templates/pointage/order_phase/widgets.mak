<%def name="order_phase_color_frame(order_phase)">
<%
order = order_phase.order
href = tg.url('/admin/order/index.html?uid={uid}'.format(uid=order.uid))
%>\
<p class="colorFrame ${order.project_cat}">\
    <span title="Commande : ${order.order_ref}">\
        Commande N° ${order.uid} -\
        <a style="color: inherit;" href="${href}" title="Afficher la commande">${order.order_ref}</a>\
    </span>\
    <span title="Phase : ${order_phase.label}">${order_phase.label}</span>\
</p>\
</%def>
