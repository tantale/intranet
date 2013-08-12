function on_accordion_refresh() {
	var index, search_list = [], searchable_node_list = $("#accordion .searchable");
	for (index = 0; index < searchable_node_list.length; ++index) {
		var keyword = $.trim($(searchable_node_list[index]).text());
		search_list.push(keyword);
	}
	$('#search_form__keyword').autocomplete({
		source : search_list
	});
	$('#search_form__keyword').val('').autocomplete('close');
}

function refresh_accordion() {
	$("#order_get_all").submit();
}

$(function() {
	$(".editInPlace").editInPlace({
		url : "http://edit"
	});

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
