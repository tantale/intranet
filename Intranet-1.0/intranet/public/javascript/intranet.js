$(function() {

	$(".edit_button").button({
		text : true
	});
	
	$(".create_button").button({
		text : true,
		icons : {
			primary : "ui-icon-check"
		}
	});

	$(".update_button").button({
		text : true,
		icons : {
			primary : "ui-icon-pencil"
		}
	});

	$(".return_button").button({
		text : true,
		icons : {
			primary : "ui-icon-arrowreturnthick-1-w"
		}
	});

	$(".new_button").button({
		text : true,
		icons : {
			primary : "ui-icon-plus"
		}
	});

	$(".delete_button").button({
		text : true,
		icons : {
			primary : "ui-icon-trash"
		}
	});

	$(".cancel_button").button({
		text : true,
		icons : {
			primary : "ui-icon-cancel"
		}
	});

	$(".search_button").button({
		text : false,
		icons : {
			primary : "ui-icon-search"
		}
	});

	if (!Modernizr.inputtypes.date) {
		$.datepicker.setDefaults($.datepicker.regional["fr"]);
		$('input[type=date]').datepicker();
	}

});
