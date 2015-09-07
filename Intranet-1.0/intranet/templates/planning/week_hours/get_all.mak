<!--
<%! import collections %>
<%flash = tg.flash_obj.render('flash', use_js=False)%>
-->
%if flash:
${flash | n}
%endif
<h2>Liste des horaires</h2>
%for week_hours in week_hours_list:
<article id="week_hours_${week_hours.uid}">
    <header>
        <p><strong>${week_hours.label}</strong></p>

        <p>${week_hours.description}</p>

        <div class="load"></div>
    </header>
</article>
<script type='text/javascript'><!--
$('#week_hours_${week_hours.uid} .load').load("${tg.url('/admin/planning/week_hours/{0}'.format(week_hours.uid))}");
-->

</script>
%endfor

