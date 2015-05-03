"use strict";
/*jslint browser: true, devel: true, es5: false, plusplus: true, unparam: true, white: true */
/*global $*/


$(function() {
	$("#toolbar_employee").button({
		text : true,
		icons : {
			primary : "ui-icon-person"
		}
	});

	$("#toolbar_order").button({
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

	$("#toolbar_chart").button({
		text : true,
		icons : {
			primary : "ui-icon-calculator"
		}
	});

	$("#toolbar_prefs").button({
		text : true,
		icons : {
			primary : "ui-icon-gear"
		}
	});
});
