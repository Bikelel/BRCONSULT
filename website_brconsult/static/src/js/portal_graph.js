/** @odoo-module **/

/**
 * Migration notes (v15 ➜ v18, option "legacy/jQuery"):
 * - On encapsule la logique dans un publicWidget (plus fiable que $(document).ready).
 * - On remplace rpc.query(...) par this._rpc({...}) (service JSON-RPC legacy exposé par publicWidget).
 * - On garde jQuery, la structure d’événements et la génération aléatoire de couleurs.
 * - On importe la session pour récupérer l'ID utilisateur.
 */

import publicWidget from "@web/legacy/js/public/public_widget";
import { session } from "@web/session";

let myChart;
let myLabels = [];
let myDatas = [];
let myColors = [];

function randomRGBList(len) {
    const out = [];
    for (let k = 0; k < len; k++) {
        const vals = [0, 0, 0].map(() => Math.floor(Math.random() * 255));
        out.push(`rgb(${vals.join(",")})`);
    }
    return out;
}

function ensureChartjs() {
    // Si Chart.js est présent via tes assets frontend, rien à faire.
    // Sinon, charge-le toi-même dans les assets ou via <script>.
    if (!window.Chart) {
        // On échoue silencieusement pour éviter une erreur JS bloquante.
        return false;
    }
    return true;
}

function drawChart(kind = "bar") {
    if (!ensureChartjs()) return;
    const ctx = document.getElementById("bar-chart-front");
    if (!ctx) return;

    if (myChart) {
        myChart.destroy();
    }
    // eslint-disable-next-line no-undef
    myChart = new Chart(ctx, {
        type: kind,
        data: {
            labels: myLabels || [],
            datasets: [
                {
                    label: "",
                    data: myDatas || [],
                    backgroundColor: myColors || [],
                    borderColor: myColors || [],
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        },
    });
}

function bar_graph() {
    drawChart("bar");
}
function line_graph() {
    drawChart("line");
}
function pie_graph() {
    drawChart("pie");
}
function doughnut_graph() {
    drawChart("doughnut");
}
function polar_graph() {
    drawChart("polarArea");
}

publicWidget.registry.BRCPortalGraph = publicWidget.Widget.extend({
    selector: "body",

    /**
     * On n’installe la logique que sur la page /my/prestations
     */
    start() {
        if (window.location.href.indexOf("/my/prestations") === -1) {
            return this._super(...arguments);
        }

        const $doc_prestation_table = $(".o_portal_my_doc_table");
        const $graph_view = $(".graph_view");
        const $graph_prestation = $(".graph_prestation");
        const $list_button = $(".list_prestation");
        const $sort_by = $("#list_sort_by");
        const $graph_option = $("#graph_options");
        const $start_date = $(".start_date");
        const $end_date = $(".end_date");
        const $group_by = $("#group_by_prestation");
        const $filter_option = $("select#filter_by_prestation");
        const $month_sep = $("a.month_seperator");
        const $year_sep = $("a.year_seperator");
        const $bar = $("button.bar_graph");
        const $line = $("button.line_graph");
        const $pie = $("button.pie_graph");
        const $doughnut = $("button.doughnut_graph");
        const $polar = $("button.polar_graph");
        const $filter = $(".fliter_by_prestation");
        const $reset = $(".reset_button_prestation");
        const $default_view = $(".no_group_prestation");

        $list_button.css("background", "black");
        $graph_option.hide();
        $graph_view.hide();
        $filter.hide();
        $bar.addClass("active_graph");

        // --- Comportement List/Graph
        $list_button.on("click", () => {
            $list_button.css("background", "black");
            $graph_prestation.css("background", "#00A09D");
            $sort_by.show();
            $graph_option.hide();
            $graph_view.hide();
            $doc_prestation_table.show();
            $(".o_portal_pager").show();
        });

        $graph_prestation.on("click", () => {
            if ($group_by.val()) {
                $graph_option.show();
            } else {
                $graph_option.hide();
            }
            $graph_prestation.css("background", "black");
            $list_button.css("background", "#00A09D");
            $sort_by.hide();
            $graph_view.show();
            $doc_prestation_table.hide();
            $(".o_portal_pager").hide();
        });

        // --- Choix du type de graphe
        $bar.on("click", () => {
            $bar.addClass("active_graph");
            $line.removeClass("active_graph");
            $pie.removeClass("active_graph");
            $doughnut.removeClass("active_graph");
            $polar.removeClass("active_graph");
            bar_graph();
        });
        $line.on("click", () => {
            $line.addClass("active_graph");
            $bar.removeClass("active_graph");
            $pie.removeClass("active_graph");
            $doughnut.removeClass("active_graph");
            $polar.removeClass("active_graph");
            line_graph();
        });
        $pie.on("click", () => {
            $pie.addClass("active_graph");
            $bar.removeClass("active_graph");
            $line.removeClass("active_graph");
            $doughnut.removeClass("active_graph");
            $polar.removeClass("active_graph");
            pie_graph();
        });
        $doughnut.on("click", () => {
            $doughnut.addClass("active_graph");
            $bar.removeClass("active_graph");
            $line.removeClass("active_graph");
            $pie.removeClass("active_graph");
            $polar.removeClass("active_graph");
            doughnut_graph();
        });
        $polar.on("click", () => {
            $polar.addClass("active_graph");
            $bar.removeClass("active_graph");
            $line.removeClass("active_graph");
            $pie.removeClass("active_graph");
            $doughnut.removeClass("active_graph");
            polar_graph();
        });

        // --- Helpers RPC
        const setGraphData = (values) => {
            if (!values) {
                $("canvas#bar-chart-front").hide();
                $.confirm({
                    title: "Error",
                    content: "Record Does not exist",
                });
                return;
            }
            const len = values.my_labels.length || 0;
            myColors = randomRGBList(len);
            myLabels = values.my_labels;
            myDatas = values.my_data;

            if ($line.hasClass("active_graph")) line_graph();
            else if ($pie.hasClass("active_graph")) pie_graph();
            else if ($doughnut.hasClass("active_graph")) doughnut_graph();
            else if ($polar.hasClass("active_graph")) polar_graph();
            else bar_graph();
        };

        // --- Séparateurs Mois / Année
        $month_sep.on("click", async () => {
            $month_sep.addClass("last_active");
            $year_sep.removeClass("last_active");
            const start_date = $("#start_date").val();
            const end_date = $("#end_date").val();
            const valid_start = new Date(start_date);
            const valid_end = new Date(end_date);
            if (valid_start <= valid_end) {
                if ($filter_option.val() === "cancelled") {
                    $filter_option.change();
                } else {
                    const values = await this._rpc({
                        model: "prestation.prestation",
                        method: "get_prestation_values_by_date",
                        args: [undefined, session.user_id, start_date, end_date, "month"],
                    });
                    setGraphData(values);
                }
            } else {
                $.confirm({ title: "Error", content: "Please ! Enter Valid Date" });
            }
        });

        $year_sep.on("click", async () => {
            $month_sep.removeClass("last_active");
            $year_sep.addClass("last_active");
            const start_date = $("#start_date").val();
            const end_date = $("#end_date").val();
            const valid_start = new Date(start_date);
            const valid_end = new Date(end_date);
            if (valid_start <= valid_end) {
                if ($filter_option.val() === "cancelled") {
                    $filter_option.change();
                } else {
                    const values = await this._rpc({
                        model: "prestation.prestation",
                        method: "get_prestation_values_by_year",
                        args: [undefined, session.user_id, start_date, end_date, "year"],
                    });
                    setGraphData(values);
                }
            } else {
                $.confirm({ title: "Error", content: "Please ! Enter Valid Date" });
            }
        });

        // --- Group By
        $group_by.on("change", async (e) => {
            const val = $(e.currentTarget).children("option:selected").val();
            if (myChart) myChart.destroy();

            if (val === "customer") {
                $reset.removeClass("d-none");
                $filter.show();
                $default_view.hide();
                $graph_option.show();
                $start_date.addClass("d-none");
                $end_date.addClass("d-none");
                $("#filter_by_prestation").val(false);

                const values = await this._rpc({
                    model: "prestation.prestation",
                    method: "get_prestation_values",
                    args: [undefined, session.user_id],
                });
                setGraphData(values);
            } else if (val === "month") {
                $filter.show();
                $reset.removeClass("d-none");
                $start_date.removeClass("d-none");
                $graph_option.show();
                $default_view.hide();
                $("#start_date").val(false);
                $("#end_date").val(false);
                $month_sep.removeClass("last_active");
                $year_sep.removeClass("last_active");
                $end_date.removeClass("d-none");
                $("#filter_by_prestation").val(false);

                const values = await this._rpc({
                    model: "prestation.prestation",
                    method: "get_prestation_month_values",
                    args: [undefined, session.user_id],
                });
                setGraphData(values);
            } else {
                $graph_option.hide();
                $default_view.show();
                $filter.hide();
                $start_date.addClass("d-none");
                $end_date.addClass("d-none");
                $reset.addClass("d-none");
            }
        });

        // --- Filter
        $filter_option.on("change", async function () {
            const groupVal = $group_by.children("option:selected").val();
            const selVal = $(this).children("option:selected").val();

            if (groupVal === "customer") {
                if (selVal === "cancelled") {
                    const values = await this._rpc({
                        model: "prestation.prestation",
                        method: "get_customer_prestation_cancelled_values",
                        args: [undefined, session.user_id],
                    });
                    setGraphData(values);
                } else {
                    $group_by.change();
                }
            } else if (groupVal === "month") {
                if (selVal === "cancelled") {
                    const start_date = $("#start_date").val();
                    const end_date = $("#end_date").val();

                    if ($year_sep.hasClass("last_active")) {
                        const values = await this._rpc({
                            model: "prestation.prestation",
                            method: "get_prestation_cancelled_values_year",
                            args: [undefined, session.user_id, start_date, end_date],
                        });
                        setGraphData(values);
                    } else if ($month_sep.hasClass("last_active")) {
                        const values = await this._rpc({
                            model: "prestation.prestation",
                            method: "get_prestation_cancelled_values_month",
                            args: [undefined, session.user_id, start_date, end_date],
                        });
                        setGraphData(values);
                    } else {
                        const values = await this._rpc({
                            model: "prestation.prestation",
                            method: "get_prestation_cancelled_values",
                            args: [undefined, session.user_id],
                        });
                        setGraphData(values);
                    }
                } else {
                    const yc = $year_sep.hasClass("last_active");
                    const mc = $month_sep.hasClass("last_active");
                    if (yc) {
                        if (selVal === "default") $year_sep.click();
                    } else if (mc) {
                        if (selVal === "default") $month_sep.click();
                    } else {
                        const values = await this._rpc({
                            model: "prestation.prestation",
                            method: "get_prestation_month_values",
                            args: [undefined, session.user_id],
                        });
                        setGraphData(values);
                    }
                }
            }
        }.bind(this));

        // --- Reset
        $("#reset_button_prestation").on("click", () => {
            $("#group_by_prestation").val(false);
            $group_by.change();
        });

        return this._super(...arguments);
    },
});

export default publicWidget.registry.BRCPortalGraph;
