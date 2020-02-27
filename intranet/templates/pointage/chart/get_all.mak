# -*- coding: utf-8 -*-
<section>
<!-- <%!
import datetime
import json
%>
<%
format_duration = lambda x: u"{0:>7s}".format(u"–.––") if x is None else u"{0:7.2f}".format(x)
format_date = lambda x: u"––/––/––––" if x is None else x.strftime(u"%d/%m/%Y")
curr_date = format_date(datetime.date.today())
%> -->
<style type="text/css" scoped="scoped">
    .duration {
        text-align: right;
    }
    .duration::after {
        content: "  ";  /* U+2002 */
    }
</style>
<div class="chart-page">

    <h2>${_(u"Statistiques des pointages")}</h2>
##
## header
##

##
## chart-table
##
    <table class="chart-table" style="page-break-inside: avoid">
        <colgroup>
            <col align="right"/>
            <col align="left"/>
            <col align="center"/>
            <col align="center"/>
        </colgroup>
        <colgroup>
            %for header in headers:
            <col align="char" char="."/>
            %endfor
        </colgroup>
        <thead>
        <tr>
            <th>${_(u"N° cmd")}</th>
            <th>${_(u"Ref. commande")}</th>
            <th>${_(u"Date de création")}</th>
            <th>${_(u"Date de clôture")}</th>
            %for header in headers:
            <th>${header}</th>
            %endfor
            <th><strong>${_(u"Total")}</strong></th>
        </tr>
        </thead>
        <tbody>
        %for order in rows:
<% order_statistics = order.statistics %>\
        <tr>
            <th>${order.uid}</th>
            <td>${order.order_ref}</td>
            <td>${format_date(order.creation_date)}</td>
            <td>${format_date(order.close_date)}</td>
            %for header in headers:
            <td class="duration">${format_duration(order_statistics.get(header))}</td>
            %endfor
            <td class="duration"><strong>${format_duration(sum(order_statistics.itervalues()))}</strong></td>
        </tr>
        %endfor
        </tbody>
        <tfoot>
        <tr>
            <th align="left" colspan="4">${_(u"TOTAL DES POINTAGES")}</th>
            %for header in headers:
            <th class="duration">${format_duration(statistics.get(header))}</th>
            %endfor
            <th class="duration"><strong>${format_duration(sum(statistics.itervalues()))}</strong></th>
        </tr>
        </tfoot>
    </table>

</div>
<script type='text/javascript'>
	"use strict";
	/*global $*/
	$(".chart-table").styleTable();
</script>
</section>