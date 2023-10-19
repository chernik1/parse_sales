
$(document).ready(function() {
    let table;
    table = $('#table').DataTable({
        "pageLength": 10,
        "order": [[0, 'asc']],
        "ordering": true,
        columns: [
            {title: "Text"},
            {title: "Number"},
            {title: "Tools"},
        ],
        dom: 'Bfrtip',
        select: {
            style: 'multi',
            selector: 'td:first-child',
            info: true,
        },
});
});
