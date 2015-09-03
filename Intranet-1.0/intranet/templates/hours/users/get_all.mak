<div>
    <!--
    <%! import collections %>
    <%flash = tg.flash_obj.render('flash', use_js=False)%>
    -->
    %if flash and not cat_group:
    ${flash | n}
    %endif
    <h2>Tableaux des horaires de travail</h2>
</div>