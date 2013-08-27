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
});
