<article id="help-article" style="font-size: .9em;">
    <header>
        <h2>${_(u"Gestion des employés")}</h2>
    </header>
    <p>${_(u"La Gestion des employés est dédiée à l'enregistrement des employés de l'entreprise. "
           u"Le nombre d'heures travaillées par semaine peut être différent d'un employé à l'autre. "
           u"S'il y a un nouvel arrivant, comme un stagiaire, on pourra l'enregistrer et indiquer "
           u"sa période de présence dans l'entreprise (date d'entrée, date de sortie).")}</p>
    <section id="help-section-01" style="margin-top: 2em;">
        <form class="minimal_form employee_get_all"
              action="${tg.url('./get_all/')}" method="get">
            <p>${_(u"Vous pouvez utiliser la zone de recherche")}
                <input type="search" name="keyword"
                       value="${keyword}"
                       placeholder="Mot-clef"
                       title="Saisir un mot-clef"/>
                <input type="hidden" name="uid" value="${uid}"/>
                <button type="submit" class="search_button_icon"
                        title="${_(u'Rechercher selon le mot-clef')}">${_(u"Rechercher")}
                </button>
                ${_(u"pour filtrer la liste des employés par leurs noms ou une partie de leurs noms.")}
            </p>
        </form>
    </section>
    <section id="help-section-02" style="margin-top: 2em;">
        <form class="minimal_form employee_new"
              action="${tg.url('./new')}" method="get">
            <p>${_(u"Cliquez sur le bouton")}
                <button id="employee_new__new" type="submit" class="new_button"
                        title="${_(u'Ajouter un nouvel employé.')}">${_(u"Nouvel employé")}
                </button>
                ${_(u"pour ajouter un nouvel employé.")}
            </p>
        </form>
        <p>${_(u"Vous pourrez alors saisir les informations suivantes\u00a0:")}</p>
        <ul>
            <li><p>${_(u"le nom de l'employé (obligatoire, sans doublon),")}</p></li>
            <li><p>${_(u"le nombre d'heures travaillées par semaine\u00a0: entre 1 et 39,")}</p></li>
            <li><p>${_(u"la date d'entrée dans l'entreprise,")}</p></li>
            <li><p>${_(u"la date de sortie (pour un employé embauché à durée déterminée, par exemple),")}</p></li>
            <li><p>${_(u"Vous pouvez aussi ajouter une photo.")}</p></li>
        </ul>
    </section>
    <section id="help-section-03" style="margin-top: 2em;">
        <p>${_(u"Dans le menu de gauche, cliquez sur l'employé que vous souhaitez modifier.")}</p>
    </section>
</article>