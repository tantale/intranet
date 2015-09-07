<div>
    <!--
    <%! import collections %>
    <%flash = tg.flash_obj.render('flash', use_js=False)%>
    -->
    %if flash:
    ${flash | n}
    %endif
    <h2>Ajouter un nouveau calendrier</h2>
</div>