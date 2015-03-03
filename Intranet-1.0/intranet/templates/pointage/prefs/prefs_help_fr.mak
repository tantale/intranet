<article id="help-article" lang="fr-FR" dir="ltr" style="font-size: .9em;">
    <header>
        <h2>Paramétrage des préférences utilisateur</h2>
    </header>
    <p>Vous pouvez paramétrer les catégories de commandes comme suit&nbsp;:</p>
    <section id="help-section-01">
        <p>Le bouton <a class="button"
                        href="${tg.url('/admin/order_cat/index.html?display=detail')}"
                        title="${_(u'Liste complète des catégories de commandes')}">${_(u"Tableau des catégories")}</a>
            vous donnera accès au paramétrage des catégories&nbsp;:</p>
        <ul>
            <li>
                <p>Ajouter ou supprimer une catégorie&nbsp;;</p>
            </li>
            <li>
                <p>Modifier le code, le libellé, la couleur de fond et la couleur du texte d’une catégorie&nbsp;;</p>
            </li>
            <li>
                <p>Ajouter ou supprimer un groupe de catégories&nbsp;;</p>
            </li>
            <li>
                <p>Modifier la liste des catégories appartenant à un groupe.</p>
            </li>
        </ul>
    </section>
    <section id="help-section-02">
        <p>Le bouton <a class="button"
                        href="${tg.url('/admin/order_cat.css?display=html')}"
                        title="${_(u'Affichage de la feuille de styles CSS des catégories de commandes')}">${_(u"Feuille de styles CSS")}</a>
            vous permettra d’afficher la feuille de styles CSS des catégories de commande.</p>
    </section>
    <section id="help-section-03">
        <p>Le bouton <a class="button"
                        href="${tg.url('/admin/order_cat/get_orphans?display=detail')}"
                        title="${_(u'Affiche la liste des commandes sans catégorie')}">${_(u"Commandes sans catégorie")}</a>
            vous permettra de rechercher les commandes qui n’ont plus de catégorie et leur en attribuer une nouvelle&nbsp;:
        </p>
        <ul>
            <li>
                <p>Sélectionner un groupe de catégories ou en créer un nouveau&nbsp;;</p>
            </li>
            <li>
                <p>Définir le libellé de la catégorie, la couleur de fond et la couleur du texte.</p>
            </li>
        </ul>
    </section>
</article>
