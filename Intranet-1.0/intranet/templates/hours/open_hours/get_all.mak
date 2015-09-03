<div>
    <!--
    <%! import collections %>
    <%flash = tg.flash_obj.render('flash', use_js=False)%>
    -->
    %if flash and not cat_group:
    ${flash | n}
    %endif
    <h2>Tableaux des horaires d’ouverture</h2>
    %for worked_hours in worked_hours_list:
    <p>${worked_hours.position} ${worked_hours.label} ${worked_hours.description}</p>
    %endfor
</div>