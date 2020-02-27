<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="${response.charset}"/>
    <title>${self.title()}</title>
    <meta name="description" content="Intranet de pointage"/>
    <link rel="icon" type="image/ico" href="${tg.url('/favicon.ico')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/blitzer/jquery-ui-1.10.3.custom.min.css')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.css')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.print.css')}" media="print"/>
    <style>
        article {
            margin: .5cm .5cm .5cm .5cm;
            padding-top: 48px;
            padding-bottom: 48px;
            padding-right: 60px;
            padding-left: 60px;
            border-radius: 6px;
            font-size: 1.8em;
            font-weight: 200;
            line-height: 1.8em;
            background-color: #eee;
        }

        header>h1 {
            display: block;
            text-align: center;
            font-size: 2em;
            line-height: normal;
            margin-bottom: 1.5cm;
            font-family: Helvetica, Arial, sans-serif;
        }

        footer {
            margin-top: 1.5cm;
            font-family: "courrier New";
            font-size: .8em;
            line-height: normal;
        }

        address {
            margin-bottom: 20px;
            font-style: normal;
            line-height: 1.2;
        }

        abbr[title] {
            cursor: help;
            border-bottom: 1px dotted #999;
        }

        .ui-menu {
            width: 400px;
        }
    </style>
</head>
<body>
<article>
    <header>
        <h1>${self.title()}</h1>
    </header>
    <section>
        ${self.content_wrapper()}\
    </section>
    <nav>
        ${self.main_menu()}\
    </nav>
    <footer>
        ${self.footer()}\
    </footer>
</article>
<script type='text/javascript' src="${tg.url('/javascript/jquery-1.9.1.js')}"></script>
<script type='text/javascript' src="${tg.url('/javascript/jquery-ui-1.10.3.custom.min.js')}"></script>
<script type='text/javascript'>
    $(function() {
      $(".menu").menu();
    });
</script>
${self.script()}
</body>
</html>

<%def name="title()">Intranet de pointage</%def>

<%def name="main_menu()">\
<h1>Menu d’accès rapide</h1>

<ul class="menu">
    <li><a href="${tg.url('/index.html')}">Accueil</a></li>
    %for menu in menus:
    <li><a title="${menu.description}">${menu.display_name}</a>
        <ul>
            %for item in menu.item_list:
            %if item.is_separator:
            <li>–</li>
            %else:
            <li><a href="${item.target_page}" title="${item.description}"><span class="ui-icon ${item.icon_name}"></span>${item.display_name}</a></li>
            %endif
            %endfor
        </ul>
    </li>
    %endfor
</ul>

</%def>

<%def name="content_wrapper()">\
<% flash = tg.flash_obj.render('flash', use_js=False) %>
%if flash:
<div class="row">
    <div class="span8 offset2">
        ${flash | n}
    </div>
</div>
%endif
${self.body()}
</%def>

<%def name="footer()">\
<hr>
<p>&copy; 2013-2014 Laurent LAPORTE – tous droits réservés –
    <small><a href="${tg.url('about.html')}">À propos de l’Intranet de pointage</a></small>.</p>
</%def>

<%def name="script()"></%def>
