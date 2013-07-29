$(function() {

	$("button[type='submit']").button({
		text : true,
		icons : {
			primary : "ui-icon-check"
		}
	});

	$("button[type='reset']").button({
		text : true,
		icons : {
			primary : "ui-icon-cancel"
		}
	});

	if (!Modernizr.inputtypes.date) {
		$('input[type=date]').datepicker();
	}

});
