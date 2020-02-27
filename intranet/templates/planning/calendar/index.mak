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
<section id="calendar">
    <section></section>
    <footer></footer>
    <script type='text/javascript'>
    $(function() {
        $('#calendar section').load("${tg.url('/admin/planning/calendar/get_all')}");
        $('#calendar footer').load("${tg.url('/admin/planning/calendar/new')}");
    });
    </script>
</section>
