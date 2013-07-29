$(function() {

	$("#toolbar_employee").button({
		text : true,
		icons : {
			primary : "ui-icon-person"
		}
	});

	$("#toolbar_command").button({
		text : true,
		icons : {
			primary : "ui-icon-document"
		}
	});

	$("#toolbar_calendar").button({
		text : true,
		icons : {
			primary : "ui-icon-calendar"
		}
	});

	$(".addButton").button({
		text : true,
		icons : {
			primary : "ui-icon-plus"
		}
	});

	$(".delButton").button({
		text : true,
		icons : {
			primary : "ui-icon-minus"
		}
	});

	$("#search_form__search").button({
		text : false,
		icons : {
			primary : "ui-icon-search"
		}
	});

	var index, search_list = [], h2_node_list = $("#accordion .searchable");

	for (index = 0; index < h2_node_list.length; ++index) {
		search_list.push($(h2_node_list[index]).text());
	}

	$("#search_form__name").autocomplete({
		source : search_list
	});

	$("#accordion").accordion({
		heightStyle : "fill"
	});
	
});
