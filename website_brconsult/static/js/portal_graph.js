var rpc;
var session;
var myChart;
var myLabels = [];
var myDatas = [];
var myColors = [];
odoo.define('website_brconsult.portal_graph', function (require) {
	"use strict";
	rpc = require('web.rpc');
	session = require('web.session');
});

$(document).ready(function () {
	var url = window.location.pathname;
	var type;
	if (window.location.href.indexOf("/my/prestations") > -1) {
		type = 'Prestations Analysis'
		var doc_prestation_table = $('.o_portal_my_doc_table');
		var graph_view = $('.graph_view');
		var graph_prestation = $('.graph_prestation');
		var list_button = $('.list_prestation');
		var sort_by = $('#list_sort_by')
		var graph_option = $("#graph_options");
		var start_date = $(".start_date");
		var end_date = $(".end_date");
		var group_by = $("#group_by_prestation");
		var filter_option = $("select#filter_by_prestation");
		var month_seperator = $('a.month_seperator');
		var year_seperator = $('a.year_seperator');
		var bar = $("button.bar_graph");
		var line = $("button.line_graph");
		var pie = $("button.pie_graph");
		var doughnut = $("button.doughnut_graph");
		var polar = $("button.polar_graph");
		var filter = $(".fliter_by_prestation")
		var reset = $(".reset_button_prestation");
		var default_view = $(".no_group_prestation");

		list_button.css('background', 'black');
		graph_option.hide()
		graph_view.hide()
		filter.hide()
		bar.addClass("active_graph");

		list_button.click(function () {
			list_button.css('background', 'black')
			graph_prestation.css('background', '#00A09D')
			sort_by.show();
			graph_option.hide()
			graph_view.hide();
			doc_prestation_table.show()
			$(".o_portal_pager").show()
		})
		graph_prestation.click(function () {
			if (group_by.val()) {
				graph_option.show();
			} else {
				graph_option.hide();
			}
			graph_prestation.css('background', 'black')
			list_button.css('background', '#00A09D')
			sort_by.hide();
			graph_view.show();
			doc_prestation_table.hide()
			$(".o_portal_pager").hide()
		})

		bar.click(function () {
			bar.addClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			bar_graph();
		})
		line.click(function () {
			line.addClass("active_graph");
			bar.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			line_graph();
		})
		pie.click(function () {
			pie.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar.removeClass("active_graph");
			pie_graph();
		})
		doughnut.click(function () {
			doughnut.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			polar.removeClass("active_graph");
			doughnut_graph();
		})
		polar.click(function () {
			polar.addClass("active_graph");
			bar.removeClass("active_graph");
			line.removeClass("active_graph");
			pie.removeClass("active_graph");
			doughnut.removeClass("active_graph");
			polar_graph();
		})

		month_seperator.click(function () {
			month_seperator.addClass("last_active");
			year_seperator.removeClass("last_active");
			var start_date = $('#start_date').val();
			var end_date = $('#end_date').val();
			var valid_start_date = new Date($('#start_date').val());
			var valid_end_date = new Date($('#end_date').val());
			if (valid_start_date <= valid_end_date) {
				if (filter_option.val() == 'cancelled') {
					filter_option.change();
				} else {
					rpc.query({
						model: 'prestation.prestation',
						method: 'get_prestation_values_by_date',
						args: [, session.user_id, start_date, end_date, 'month'],
					}).then(function (values) {
						if (values) {
							var my_length = values['my_labels'].length;
							var i = 0;
							var rgb = [];
							for (var k = 0; k < my_length; k++) {
								var rgb_val = [];
								var rgb_vals = [];
								for (i = 0; i < 3; i++) {
									rgb_vals.push(Math.floor(Math.random() * 255));
								}
								var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
								rgb_val += rgb_val_joined;
								rgb.push(rgb_val);
							}
							myColors = rgb;
							myLabels = values['my_labels'];
							myDatas = values['my_data'];
							var l = line.hasClass("active_graph");
							var pi = pie.hasClass("active_graph");
							var d = doughnut.hasClass("active_graph");
							var p = polar.hasClass("active_graph");
							if (l) {
								line_graph()
							} else if (pi) {
								pie_graph()
							} else if (d) {
								doughnut_graph()
							} else if (p) {
								polar_graph()
							} else {
								bar_graph()
							}
						} else {
							$("canvas#bar-chart-front").hide();
							$.confirm({
								title: 'Error',
								content: 'Record Does not exits',
							});
						}
					});
				}
			} else {
				$.confirm({
					title: 'Error',
					content: 'Please ! Enter Valid Date',
				});
			}
		})

		year_seperator.click(function () {
			month_seperator.removeClass("last_active");
			year_seperator.addClass("last_active");
			var start_date = $('#start_date').val();
			var end_date = $('#end_date').val();
			var valid_start_date = new Date($('#start_date').val());
			var valid_end_date = new Date($('#end_date').val());
			if (valid_start_date <= valid_end_date) {
				if (filter_option.val() == 'cancelled') {
					filter_option.change();
				} else {
					rpc.query({
						model: 'prestation.prestation',
						method: 'get_prestation_values_by_year',
						args: [, session.user_id, start_date, end_date, 'year'],
					}).then(function (values) {
						if (values) {
							var my_length = values['my_labels'].length;
							var i = 0;
							var rgb = [];
							for (var k = 0; k < my_length; k++) {
								var rgb_val = [];
								var rgb_vals = [];
								for (i = 0; i < 3; i++) {
									rgb_vals.push(Math.floor(Math.random() * 255));
								}
								var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
								rgb_val += rgb_val_joined;
								rgb.push(rgb_val);
							}
							myColors = rgb;
							myLabels = values['my_labels'];
							myDatas = values['my_data'];
							var l = line.hasClass("active_graph");
							var pi = pie.hasClass("active_graph");
							var d = doughnut.hasClass("active_graph");
							var p = polar.hasClass("active_graph");
							if (l) {
								line_graph()
							} else if (pi) {
								pie_graph()
							} else if (d) {
								doughnut_graph()
							} else if (p) {
								polar_graph()
							} else {
								bar_graph()
							}
						} else {
							$("canvas#bar-chart-front").hide();
							$.confirm({
								title: 'Error',
								content: 'Record Not Found',
							});
						}
					});
				}
			} else {
				$.confirm({
					title: 'Error',
					content: 'Please ! Enter Valid Date',
				});
			}
		});

		group_by.change(function () {
			var val = $(this).children("option:selected").val();
			if (myChart) {
				myChart.destroy();
			}
			if (val == 'customer') {
				reset.removeClass('d-none')
				filter.show();
				default_view.hide();
				graph_option.show();
				start_date.addClass("d-none");
				end_date.addClass("d-none");
				$("#filter_by_prestation").val(false)
				rpc.query({
					model: 'prestation.prestation',
					method: 'get_prestation_values',
					args: [, session.user_id],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data'];
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				});
			} else if (val == 'month') {
				filter.show()
				reset.removeClass('d-none')
				start_date.removeClass("d-none");
				graph_option.show();
				default_view.hide();
				$("#start_date").val(false);
				$("#end_date").val(false);
				month_seperator.removeClass("last_active");
				year_seperator.removeClass("last_active");
				end_date.removeClass("d-none");
				$("#filter_by_prestation").val(false)
				rpc.query({
					model: 'prestation.prestation',
					method: 'get_prestation_month_values',
					args: [, session.user_id],
				}).then(function (values) {
					if (values) {
						var my_length = values['my_labels'].length;
						var i = 0;
						var rgb = [];
						for (var k = 0; k < my_length; k++) {
							var rgb_val = [];
							var rgb_vals = [];
							for (i = 0; i < 3; i++) {
								rgb_vals.push(Math.floor(Math.random() * 255));
							}
							var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
							rgb_val += rgb_val_joined;
							rgb.push(rgb_val);
						}
						myColors = rgb;
						myLabels = values['my_labels'];
						myDatas = values['my_data']
						var l = line.hasClass("active_graph");
						var pi = pie.hasClass("active_graph");
						var d = doughnut.hasClass("active_graph");
						var p = polar.hasClass("active_graph");
						if (l) {
							line_graph()
						} else if (pi) {
							pie_graph()
						} else if (d) {
							doughnut_graph()
						} else if (p) {
							polar_graph()
						} else {
							bar_graph()
						}
					} else {
						$("canvas#bar-chart-front").hide();
						$.confirm({
							title: 'Error',
							content: 'Record Does not exits',
						});
					}
				});
			} else {
				graph_option.hide();
				default_view.show();
				filter.hide();
				start_date.addClass("d-none");
				end_date.addClass("d-none");
				reset.addClass('d-none')
			}
		})

		filter_option.change(function () {
			var val = group_by.children("option:selected").val();
			var sel_val = $(this).children("option:selected").val();
			if (val == 'customer') {
				if (sel_val === 'cancelled') {
					rpc.query({
						model: 'prestation.prestation',
						method: 'get_customer_prestation_cancelled_values',
						args: [, session.user_id],
					}).then(function (values) {
						if (values) {
							var my_length = values['my_labels'].length;
							var i = 0;
							var rgb = [];
							for (var k = 0; k < my_length; k++) {
								var rgb_val = [];
								var rgb_vals = [];
								for (i = 0; i < 3; i++) {
									rgb_vals.push(Math.floor(Math.random() * 255));
								}
								var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
								rgb_val += rgb_val_joined;
								rgb.push(rgb_val);
							}
							myColors = rgb;
							myLabels = values['my_labels'];
							myDatas = values['my_data']
							var l = line.hasClass("active_graph");
							var pi = pie.hasClass("active_graph");
							var d = doughnut.hasClass("active_graph");
							var p = polar.hasClass("active_graph");
							if (l) {
								line_graph()
							} else if (pi) {
								pie_graph()
							} else if (d) {
								doughnut_graph()
							} else if (p) {
								polar_graph()
							} else {
								bar_graph()
							}
						} else {
							$("canvas#bar-chart-front").hide();
							$.confirm({
								title: 'Error',
								content: 'Record Does not exits',
							});
						}
					});
				} else {
					group_by.change();
				}
			} else if (val == 'month') {
				if (sel_val === 'cancelled') {
					var m = month_seperator.hasClass("last_active")
					var y = year_seperator.hasClass("last_active")
					if (y) {
						var start_date = $('#start_date').val();
						var end_date = $('#end_date').val();
						rpc.query({
							model: 'prestation.prestation',
							method: 'get_prestation_cancelled_values_year',
							args: [, session.user_id, start_date, end_date],
						}).then(function (values) {
							if (values) {
								var my_length = values['my_labels'].length;
								var i = 0;
								var rgb = [];
								for (var k = 0; k < my_length; k++) {
									var rgb_val = [];
									var rgb_vals = [];
									for (i = 0; i < 3; i++) {
										rgb_vals.push(Math.floor(Math.random() * 255));
									}
									var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
									rgb_val += rgb_val_joined;
									rgb.push(rgb_val);
								}
								myColors = rgb;
								myLabels = values['my_labels'];
								myDatas = values['my_data']
								var l = line.hasClass("active_graph");
								var pi = pie.hasClass("active_graph");
								var d = doughnut.hasClass("active_graph");
								var p = polar.hasClass("active_graph");
								if (l) {
									line_graph()
								} else if (pi) {
									pie_graph()
								} else if (d) {
									doughnut_graph()
								} else if (p) {
									polar_graph()
								} else {
									bar_graph()
								}
							} else {
								$("canvas#bar-chart-front").hide();
								$.confirm({
									title: 'Error',
									content: 'Record Does not exits',
								});
							}
						});
					} else if (m) {
						var start_date = $('#start_date').val();
						var end_date = $('#end_date').val();
						rpc.query({
							model: 'prestation.prestation',
							method: 'get_prestation_cancelled_values_month',
							args: [, session.user_id, start_date, end_date],
						}).then(function (values) {
							if (values) {
								var my_length = values['my_labels'].length;
								var i = 0;
								var rgb = [];
								for (var k = 0; k < my_length; k++) {
									var rgb_val = [];
									var rgb_vals = [];
									for (i = 0; i < 3; i++) {
										rgb_vals.push(Math.floor(Math.random() * 255));
									}
									var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
									rgb_val += rgb_val_joined;
									rgb.push(rgb_val);
								}
								myColors = rgb;
								myLabels = values['my_labels'];
								myDatas = values['my_data']
								var l = line.hasClass("active_graph");
								var pi = pie.hasClass("active_graph");
								var d = doughnut.hasClass("active_graph");
								var p = polar.hasClass("active_graph");
								if (l) {
									line_graph()
								} else if (pi) {
									pie_graph()
								} else if (d) {
									doughnut_graph()
								} else if (p) {
									polar_graph()
								} else {
									bar_graph()
								}
							} else {
								$("canvas#bar-chart-front").hide();
								$.confirm({
									title: 'Error',
									content: 'Record Does not exits',
								});
							}
						});
					} else {
						rpc.query({
							model: 'prestation.prestation',
							method: 'get_prestation_cancelled_values',
							args: [, session.user_id],
						}).then(function (values) {
							if (values) {
								var my_length = values['my_labels'].length;
								var i = 0;
								var rgb = [];
								for (var k = 0; k < my_length; k++) {
									var rgb_val = [];
									var rgb_vals = [];
									for (i = 0; i < 3; i++) {
										rgb_vals.push(Math.floor(Math.random() * 255));
									}
									var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
									rgb_val += rgb_val_joined;
									rgb.push(rgb_val);
								}
								myColors = rgb;
								myLabels = values['my_labels'];
								myDatas = values['my_data']
								var l = line.hasClass("active_graph");
								var pi = pie.hasClass("active_graph");
								var d = doughnut.hasClass("active_graph");
								var p = polar.hasClass("active_graph");
								if (l) {
									line_graph()
								} else if (pi) {
									pie_graph()
								} else if (d) {
									doughnut_graph()
								} else if (p) {
									polar_graph()
								} else {
									bar_graph()
								}
							} else {
								$("canvas#bar-chart-front").hide();
								$.confirm({
									title: 'Error',
									content: 'Record Does not exits',
								});
							}
						});
					}
				} else {
					var mc = month_seperator.hasClass("last_active");
					var yc = year_seperator.hasClass("last_active");
					if (yc) {
						if (sel_val == 'default') {
							year_seperator.click()
						}
					} else if (mc) {
						if (sel_val == 'default') {
							month_seperator.click()
						}
					} else {
						rpc.query({
							model: 'prestation.prestation',
							method: 'get_prestation_month_values',
							args: [, session.user_id],
						}).then(function (values) {
							if (values) {
								var my_length = values['my_labels'].length;
								var i = 0;
								var rgb = [];
								for (var k = 0; k < my_length; k++) {
									var rgb_val = [];
									var rgb_vals = [];
									for (i = 0; i < 3; i++) {
										rgb_vals.push(Math.floor(Math.random() * 255));
									}
									var rgb_val_joined = 'rgb(' + rgb_vals.join(',') + ')';
									rgb_val += rgb_val_joined;
									rgb.push(rgb_val);
								}
								myColors = rgb;
								myLabels = values['my_labels'];
								myDatas = values['my_data'];
								var l = line.hasClass("active_graph");
								var pi = pie.hasClass("active_graph");
								var d = doughnut.hasClass("active_graph");
								var p = polar.hasClass("active_graph");
								if (l) {
									line_graph()
								} else if (pi) {
									pie_graph()
								} else if (d) {
									doughnut_graph()
								} else if (p) {
									polar_graph()
								} else {
									bar_graph()
								}
							} else {
								$("canvas#bar-chart-front").hide();
								$.confirm({
									title: 'Error',
									content: 'Record Does not exits',
								});
							}
						});
					}
				}
			}
		})

		$("#reset_button_prestation").click(function () {
			$("#group_by_prestation").val(false);
			group_by.change();
		})
	
	}
});