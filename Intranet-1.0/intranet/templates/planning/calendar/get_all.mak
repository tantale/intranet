%for calendar in calendar_list:
<tr id="calendar_${calendar.uid}"></tr>
<script type='text/javascript'>
$(function() {
    $('#calendar_${calendar.uid}').load("${tg.url('/admin/planning/calendar/{0}/edit'.format(calendar.uid))}");
});
</script>
%endfor
