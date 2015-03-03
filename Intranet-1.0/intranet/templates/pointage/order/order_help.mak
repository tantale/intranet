<article id="help-article" style="font-size: .9em;">
    <header>
        <h2>${_(u"Gestion des commandes")}</h2>
    </header>
    <p>${_(u"La Gestion des commandes permet d'enregistrer les commandes en cours "
           u"mais aussi les devis. Une commande est divisée en phases allant de la "
           u"commercialisation à la livraison. Les tâches internes à l'entreprise "
           u"qui nécessiteront un pointage, comme le déchargement, l'aménagement "
           u"des bureaux, le rangement de l'atelier, seront aussi enregistrées "
           u"dans la gestion des commandes. Enfin, on utilisera une commande fictive "
           u"«\u00a0Absence\u00a0» (par exemple) pour pointer les jours de congé, "
           u"les jours fériés, les absences maladie, etc.")}</p>
    <section id="help-section-01" style="margin-top: 2em;">
        <form class="minimal_form order_get_all"
              action="${tg.url('./get_all/')}" method="get">
            <p>${_(u"Vous pouvez utiliser la zone de recherche")}
                <input type="number" name="uid"
                       value="${uid}"
                       placeholder="N° commande"
                       title="${_(u'Numéro de la commande recherchée')}"/>
                ${_(u"pour retrouver rapidement une commande en fonction de son numéro,")}
                ${_(u"ou la zone de recherche")}
                <input type="search" name="keyword"
                       value="${keyword}"
                       placeholder="Mot-clef"
                       title="${_(u'Saisir un mot-clef')}"/>
                <input type="hidden" name="order_ref" value=""/>
                <button type="submit" class="search_button"
                        title="${_(u'Rechercher selon le mot-clef')}">${_(u"Rechercher")}
                </button>
                ${_(u"pour filtrer la liste des commandes par leurs références ou une partie de leurs références.")}
            </p>
        </form>
    </section>
    <section id="help-section-02" style="margin-top: 2em;">
        <form class="minimal_form order_new"
              action="${tg.url('./new')}" method="get">
            <p>${_(u"Cliquez sur le bouton")}
                <button type="submit" class="new_button"
                        title="${_(u'Ajouter une nouvelle commande.')}">${_(u"Nouvelle commande")}
                </button>
                ${_(u"pour ajouter une nouvelle commande.")}
            </p>
        </form>
        <p>${_(u"Vous pourrez alors saisir les informations suivantes\u00a0:")}</p>
        <ul>
            <li><p>${_(u"la référence de la commande (obligatoire, sans doublon),")}</p></li>
            <li><p>${_(u"la catégorie de commande (Magasin, Bureau, Dressing, etc.),")}</p></li>
            <li><p>${_(u"la date de création de la commande,")}</p></li>
            <li><p>${_(u"la date de clôture de la commande (si elle est connue).")}</p></li>
        </ul>
    </section>
    <section id="help-section-03" style="margin-top: 2em;">
        <p>${_(u"Dans le menu de gauche, cliquez sur la commande que vous souhaitez modifier.")}</p>

        <p>${_(u"La liste des phases est modifiable\u00a0:")}</p>
        <ul>
            <li><p>${_(u"Modifiez une phase en cliquant sur son libellé, "
                       u"appuyez sur la touche «\u00a0Entrée\u00a0» pour valider.")}</p></li>
            <li><p>${_(u"Supprimez une phase en cliquant sur son libellé, "
                       u"puis sur la croix «\u00a0×\u00a0» pour effacer, "
                       u"puis appuyez sur la touche «\u00a0Entrée\u00a0» pour valider.")}</p></li>
            <li><p>${_(u"Modifiez l'ordre des phases en cliquant sur le curseur «\u00a0Haut / Bas\u00a0». "
                       u"Cela a pour effet d'amorcer un glisser / déposer. Déposez la phase à l'endroit "
                       u"que vous souhaitez.")}</p></li>
            <li><p>${_(u"Ajoutez une nouvelle phase en saisissant son libellé puis en cliquant "
                       u" sur le bouton «\u00a0+\u00a0» (ajouter).")}</p></li>
        </ul>
    </section>
</article>