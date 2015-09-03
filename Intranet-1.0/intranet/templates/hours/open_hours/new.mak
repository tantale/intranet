<div>
    <!--
    <%! import collections %>
    <%flash = tg.flash_obj.render('flash', use_js=False)%>
    -->
    %if flash and not cat_group:
    ${flash | n}
    %endif
    <h2>Ajouter de nouvelles horaires d’ouverture</h2>
</div>