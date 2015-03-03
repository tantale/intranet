<article id="help-article" lang="fr-FR" dir="ltr" style="font-size: .9em;">
    <header>
        <h2>${_(u"Paramétrage des préférences utilisateur")}</h2>
    </header>
    <p>${_(u"Vous pouvez paramétrer les catégories de commandes comme suit\u00a0:")}</p>
    <section id="help-section-01">
        <p>${_(u"Le bouton ")}<a class="button"
                                 href="${tg.url('/admin/order_cat/index.html?display=detail')}"
                                 title="${_(u'Liste complète des catégories de commandes')}">${_(u"Tableau des catégories")}</a>
            ${_(u"vous donnera accès au paramétrage des catégories\u00a0:")}</p>
        <ul>
            <li>
                <p>${_(u"Ajouter ou supprimer une catégorie\u00a0;")}</p>
            </li>
            <li>
                <p>
                    ${_(u"Modifier le code, le libellé, la couleur de fond et la couleur du texte d’une catégorie\u00a0;")}</p>
            </li>
            <li>
                <p>${_(u"Ajouter ou supprimer un groupe de catégories\u00a0;")}</p>
            </li>
            <li>
                <p>${_(u"Modifier la liste des catégories appartenant à un groupe.")}</p>
            </li>
        </ul>
    </section>
    <section id="help-section-02">
        <p>${_(u"Le bouton ")}<a class="button"
                                 href="${tg.url('/admin/order_cat/get_orphans?display=detail')}"
                                 title="${_(u'Affiche la liste des commandes sans catégorie')}">${_(u"Commandes sans catégorie")}</a>
            ${_(u"vous permettra de rechercher les commandes qui n’ont plus de catégorie et leur en attribuer une nouvelle\u00a0:")}
        </p>
        <ul>
            <li>
                <p>${_(u"Sélectionner un groupe de catégories ou en créer un nouveau\u00a0;")}</p>
            </li>
            <li>
                <p>${_(u"Définir le libellé de la catégorie, la couleur de fond et la couleur du texte.")}</p>
            </li>
        </ul>
    </section>
    <section id="help-section-03">
        <p>${_(u"Le bouton ")}<a class="button"
                                 href="${tg.url('/admin/order_cat.css?display=html')}"
                                 title="${_(u'Affichage de la feuille de styles CSS des catégories de commandes')}">${_(u"Feuille de styles CSS")}</a>
            ${_(u"vous permettra d’afficher la feuille de styles CSS des catégories de commande.")}</p>
    </section>
</article>
