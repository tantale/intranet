<div>
    <!--
    <%! import collections %>
    <%flash = tg.flash_obj.render('flash', use_js=False)%>
    -->
    %if flash and not cat_group:
    ${flash | n}
    %endif
    <h2>Liste des calendriers</h2>
    %for calendar in calendar_list:
    <p>${calendar.position} ${calendar.label} ${calendar.description}</p>
    %endfor
</div>
