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

	var index, search_list = [], searchable_node_list = $("#accordion .searchable");

	for (index = 0; index < searchable_node_list.length; ++index) {
		var keyword = $.trim($(searchable_node_list[index]).text());
		search_list.push(keyword);
	}

	$("#search_form__keyword").autocomplete({
		source : search_list
	});

	$("#accordion").accordion({
		heightStyle : "fill"
	});
	
});
