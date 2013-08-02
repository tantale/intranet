function display_employee_create_form(event) {
	if (event) {
		event.preventDefault();
	}
	$("#employee_update").hide();
	$(".create_button").button("disable");
	$("#employee_create").show().focus();
}

function display_employee_update_form(event) {
	if (event) {
		event.preventDefault();
	}
	$("#employee_create").hide();
	$(".create_button").button("enable");
	$("#employee_update").show().focus();
}

$(function() {
	$(".picture_placeholder").imgLiquid({
		fill : true,
		horizontalAlign : "center",
		verticalAlign : "center"
	});

	$(".create_button").click(display_employee_create_form);
	$("#employee_create__cancel").click(display_employee_update_form);

	$('body').layout({
		north__size : "auto",
		north__closable : false,
		north__resizable : false,
		north__slidable : false,
		north__spacing_open : 0,
		north__spacing_closed : 0,

		west__size : 260,
		west__minSize : 230,
		west__maxSize : 500
	});

});
