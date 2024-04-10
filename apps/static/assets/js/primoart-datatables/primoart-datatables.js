sandboxMainDashTable = {
    init: function() {
        $('#dashboard-events').DataTable( {
            "language": {
                "decimal":        "",
                "emptyTable":     "No data available in table",
                "info":           "_START_-_END_ из _TOTAL_ событий",
                "infoEmpty":      "Showing 0 to 0 of 0 entries",
                "infoFiltered":   "(filtered from _MAX_ total entries)",
                "infoPostFix":    "",
                "thousands":      ",",
                "lengthMenu":     "Показать _MENU_ событий",
                "loadingRecords": "Loading...",
                "processing":     "",
                "search":         "Поиск:",
                "zeroRecords":    "No matching records found",
                "aria": {
                    "orderable":  "Order by this column",
                    "orderableReverse": "Reverse order this column"
                }
            }
        });
    }
}

objectsProjectsTable = {
    init: function() {
        $('#projects-table').DataTable( {
            "language": {
                "decimal":        "",
                "emptyTable":     "No data available in table",
                "info":           "_START_-_END_ из _TOTAL_ проектов",
                "infoEmpty":      "Showing 0 to 0 of 0 entries",
                "infoFiltered":   "(filtered from _MAX_ total entries)",
                "infoPostFix":    "",
                "thousands":      ",",
                "lengthMenu":     "Показать _MENU_ проектов",
                "loadingRecords": "Loading...",
                "processing":     "",
                "search":         "Поиск:",
                "zeroRecords":    "No matching records found",
                "aria": {
                    "orderable":  "Order by this column",
                    "orderableReverse": "Reverse order this column"
                }
            }
        });
    }
}


objectsServicesTable = {
    init: function(tableId) {

        var table = document.getElementById(tableId);
        $(table).DataTable( {
            "language": {
                "decimal":        "",
                "emptyTable":     "No data available in table",
                "info":           "_START_-_END_ из _TOTAL_ сервисов",
                "infoEmpty":      "Showing 0 to 0 of 0 entries",
                "infoFiltered":   "(filtered from _MAX_ total entries)",
                "infoPostFix":    "",
                "thousands":      ",",
                "lengthMenu":     "Показать _MENU_ сервисов",
                "loadingRecords": "Loading...",
                "processing":     "",
                "search":         "Поиск:",
                "zeroRecords":    "No matching records found",
                "aria": {
                    "orderable":  "Order by this column",
                    "orderableReverse": "Reverse order this column"
                }
            }
        });
    }
}