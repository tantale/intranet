<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Strict//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>${_(u"Contrôle du pointage de {employee_name}").format(employee_name=employee_name)}</title>
    <link rel="icon" type="image/ico" href="${tg.url('/favicon.ico')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/blitzer/jquery-ui-1.10.3.custom.min.css')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.css')}"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.print.css')}" media="print"/>
    <link rel="stylesheet" type="text/css" href="${tg.url('/css/intranet.pointage.css')}"/>
    <script type='text/javascript' src="${tg.url('/javascript/jquery-1.9.1.js')}"></script>
    <script type='text/javascript' src="${tg.url('/javascript/jquery-ui-1.10.3.custom.min.js')}"></script>
    <script type='text/javascript' src="${tg.url('/javascript/intranet.js')}"></script>
</head>
<body>
<div class="page">
    <%include file="local:templates.pointage.trcal.ctrl_rec_times"/>
</div>
<script type='text/javascript'>
    "use strict";
    /*global $*/
    $(function() {
        window.print();
    });
</script>
</body>
</html>