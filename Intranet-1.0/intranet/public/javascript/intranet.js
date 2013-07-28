$(function() {

	$("button[type='submit']").button({
		text : true,
		icons : {
			primary : "ui-icon-check"
		}
	});

	if (!Modernizr.inputtypes.date) {
		$('input[type=date]').datepicker();
	}

});
