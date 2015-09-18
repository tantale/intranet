<style scoped="scoped">
    article {
        border-bottom-width: 1px;
        border-bottom-style: dashed;
        border-bottom-color: #CC0000;
        padding-bottom: 1em;
    }
    article p {
        margin: 0.3em 0 .5em 0;
    }
    article h2 .label {
        font-family: arial;
        font-size: 1em;
        font-weight: bold;
        width: 14em;
    }
    article p .description {
        font-family: arial;
        font-size: 1em;
        width: 36em;
    }
    article p label {
        display: inline-block;
        font-family: arial;
        font-size: 1em;
        width: 12.5em;
    }
    article nav {
        padding-top: 1em;
    }
</style>
<style scoped="scoped">
    .ts-time {text-align: right;}
    .ts-start {color: rgb(238, 130, 14);}
    .ts-end {color: rgb(8, 151, 59);}
    .ts-delta {color: rgb(18, 151, 214);}
    .ts-interval-invalid {
        background-color: #f2dede;
        border-color: #eed3d7;
        color: #b94a48;
    }
    .styletable { border-collapse: separate; }
    .styletable td { font-weight: normal !important; padding: .4em; border-top-width: 0px !important; }
    .styletable th { text-align: center; padding: .8em .4em; }
    .styletable td.first, .styletable th.first { border-left-width: 0px !important; }
</style>
<section id="week_hours">
    <section></section>
    <footer></footer>
    <script type='text/javascript'>
    $(function() {
        $('#week_hours section').load("${tg.url('/admin/planning/week_hours/get_all')}");
        $('#week_hours footer').load("${tg.url('/admin/planning/week_hours/new')}");
    });
    </script>
</section>
