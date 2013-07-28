$(function() {
	$(".picture_placeholder").imgLiquid({
		fill : true,
		horizontalAlign : "center",
		verticalAlign : "center"
	});

	$(".selectEmpButton").button({
		text : true
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
