"use strict";
/*jslint browser: true, devel: true, es5: false, plusplus: true, unparam: true, white: true */
/*global $*/

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

	$(".update_button_icon").button({
		text : false,
		icons : {
			primary : "ui-icon-pencil"
		}
	});

	$(".refresh_button").button({
		text : false,
		icons : {
			primary : "ui-icon-refresh"
		}
	});

	$(".new_button").button({
		text : true,
		icons : {
			primary : "ui-icon-plus"
		}
	});

	$(".new_button_icon").button({
		text : false,
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

	$(".delete_button_icon").button({
		text : false,
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

	$(".cancel_button_icon").button({
		text : false,
		icons : {
			primary : "ui-icon-cancel"
		}
	});

	$(".search_button").button({
		text : true,
		icons : {
			primary : "ui-icon-search"
		}
	});

	$(".search_button_icon").button({
		text : false,
		icons : {
			primary : "ui-icon-search"
		}
	});

	$(".refresh_button").button({
		text : true,
		icons : {
			primary : "ui-icon-refresh"
		}
	});

	$(".refresh_button_icon").button({
		text : false,
		icons : {
			primary : "ui-icon-refresh"
		}
	});

	$(".calendar_button").button({
		text : true,
		icons : {
			primary : "ui-icon-calendar"
		}
	});

	$(".calendar_button_icon").button({
		text : false,
		icons : {
			primary : "ui-icon-calendar"
		}
	});

});

(function ($) {
	$.fn.styleTable = function (options) {
		var defaults = {
			css: 'styleTable'
		};
		options = $.extend(defaults, options);

		return this.each(function () {
			var input = $(this);
			input.addClass(options.css);
			input.find("tr").on('mouseover mouseout', function (event) {
				if (event.type == 'mouseover') {
					$(this).children("td").addClass("ui-state-hover");
				} else {
					$(this).children("td").removeClass("ui-state-hover");
				}
			});
			input.find("th").addClass("ui-state-default");
			input.find("td").addClass("ui-widget-content");
			input.find("tr").each(function () {
				$(this).children("td:not(:first)").addClass("first");
				$(this).children("th:not(:first)").addClass("first");
			});
		});
	};
})(jQuery);
