
$(document).ready(function() {


  let table = $('#table').DataTable({
    "pageLength": 100,
    "order": [[0, 'asc']],
    "ordering": true,
    columns: [
        {title: "Keyword"},
        {title: "Регистрационный номер"},
        {title: "Имя компании"},
        {title: 'УНП'},
        {title: "Предмет"},
        {title: "Дата"},
        {title: "Цена"},
    ],
    dom: 'Bfrtip',
    select: {
        style: 'multi',
        selector: 'td:first-child',
        info: true,
    },
    buttons: [
        {
            text: 'Delete',
            className: 'button-table-delete',
            action: function (e, dt, node, config) {
                let dataTable;
                dataTable = document.querySelectorAll('#table');
                let selectedIds = [];
                let selectedRows = dt.rows({selected: true}).nodes();
                selectedRows.each(function(row) {
                    let tdElement = row.querySelector('td[data-id_purchase]');
                    let rowId = tdElement.getAttribute('data-id_purchase');
                    selectedIds.push(rowId);
                });
                deleteFunction(selectedIds, dataTable);
            }
        },
        {
            text: 'Delete all',
            className: 'button-table-delete-all',
            action: function (e, dt, node, config) {
                deleteAllFunction();
            }
        },
        {
            text: 'Завершить',
            className: 'button-table-complete',
            action: function (e, dt, node, config){
                let dataTable;
                dataTable = document.querySelectorAll('#table');
                let selectedIds = [];
                let selectedRows = dt.rows({selected: true}).nodes();
                selectedRows.each(function(row) {
                    let tdElement = row.querySelector('td[data-id_purchase]');
                    let rowId = tdElement.getAttribute('data-id_purchase');
                    selectedIds.push(rowId);
                });
                completeFunction(selectedIds, dataTable);
            }
        }
    ]
});

function completeFunction(id_list, dataTable){
   $.ajax({
        url: "/complete/",
        type: "POST",
        data: {
            id_list: id_list,
            data_table: dataTable,
        },
        dataType: "json",
        success: function(response) {
            table.clear();
            response.table.forEach(function(item) {
                let row = document.createElement('tr');

                let keywordCell = document.createElement('td');
                keywordCell.setAttribute('data-keyword', item.keyword);
                keywordCell.textContent = item.keyword;
                row.appendChild(keywordCell);

                let idPurchaseCell = document.createElement('td');
                idPurchaseCell.setAttribute('data-id_purchase', item.id_purchase);
                idPurchaseCell.textContent = item.id_purchase;
                row.appendChild(idPurchaseCell);

                let nameCompanyCell = document.createElement('td');
                nameCompanyCell.setAttribute('data-name_company', item.name_company);
                nameCompanyCell.textContent = item.name_company;
                row.appendChild(nameCompanyCell);

                let namePurchaseCell = document.createElement('td');
                namePurchaseCell.setAttribute('data-name_purchase', item.name_purchase);
                namePurchaseCell.textContent = item.name_purchase;
                row.appendChild(namePurchaseCell);

                let dateCell = document.createElement('td');
                dateCell.setAttribute('data-date', item.date);
                dateCell.textContent = item.date;
                row.appendChild(dateCell);

                let priceCell = document.createElement('td');
                priceCell.setAttribute('data-price', item.price);
                priceCell.textContent = item.price;
                row.appendChild(priceCell);

                let payerNumberCell = document.createElement('td');
                payerNumberCell.setAttribute('data-payer-number', item.payer_number);
                payerNumberCell.textContent = item.payer_number;
                row.appendChild(payerNumberCell);

                table.row.add(row);
            });
            table.draw();
        }
    });
};

    function deleteFunction(id_list, dataTable) {
    $.ajax({
        url: "/delete/",
        type: "POST",
        data: {
            id_list: id_list,
            data_table: dataTable,
        },
        dataType: "json",
        success: function(response) {
            table.clear();
            response.table.forEach(function(item) {
                let row = document.createElement('tr');

                let keywordCell = document.createElement('td');
                keywordCell.setAttribute('data-keyword', item.keyword);
                keywordCell.textContent = item.keyword;
                row.appendChild(keywordCell);

                let idPurchaseCell = document.createElement('td');
                idPurchaseCell.setAttribute('data-id_purchase', item.id_purchase);
                idPurchaseCell.textContent = item.id_purchase;
                row.appendChild(idPurchaseCell);

                let nameCompanyCell = document.createElement('td');
                nameCompanyCell.setAttribute('data-name_company', item.name_company);
                nameCompanyCell.textContent = item.name_company;
                row.appendChild(nameCompanyCell);

                let namePurchaseCell = document.createElement('td');
                namePurchaseCell.setAttribute('data-name_purchase', item.name_purchase);
                namePurchaseCell.textContent = item.name_purchase;
                row.appendChild(namePurchaseCell);

                let dateCell = document.createElement('td');
                dateCell.setAttribute('data-date', item.date);
                dateCell.textContent = item.date;
                row.appendChild(dateCell);

                let priceCell = document.createElement('td');
                priceCell.setAttribute('data-price', item.price);
                priceCell.textContent = item.price;
                row.appendChild(priceCell);

                let payerNumberCell = document.createElement('td');
                payerNumberCell.setAttribute('data-payer-number', item.payer_number);
                payerNumberCell.textContent = item.payer_number;
                row.appendChild(payerNumberCell);

                table.row.add(row);
            });
            table.draw();
        }
    });
}

function deleteAllFunction() {
    $.ajax({
        url: "/delete_all/",
        type: "GET",
        dataType: "json",
        success: function(response) {
            table.clear();
            table.draw();
        }
    });
}


document.getElementById('start-button').addEventListener('click', function() {
    let dataTable = document.getElementById('table');
    $.ajax({
        url: 'data/',
        type: 'POST',
        data: {
            data_table: dataTable.innerHTML,
        },
        dataType: "json",
        success: function(response) {
            let table = $('#table').DataTable();
            table.clear();

            response.table.forEach(function(item) {
                let row = document.createElement('tr');

                let keywordCell = document.createElement('td');
                keywordCell.setAttribute('data-keyword', item.keyword);
                keywordCell.textContent = item.keyword;
                row.appendChild(keywordCell);

                let idPurchaseCell = document.createElement('td');
                idPurchaseCell.setAttribute('data-id_purchase', item.id_purchase);
                idPurchaseCell.textContent = item.id_purchase;
                row.appendChild(idPurchaseCell);

                let nameCompanyCell = document.createElement('td');
                nameCompanyCell.setAttribute('data-name_company', item.name_company);
                nameCompanyCell.textContent = item.name_company;
                row.appendChild(nameCompanyCell);

                let namePurchaseCell = document.createElement('td');
                namePurchaseCell.setAttribute('data-name_purchase', item.name_purchase);
                namePurchaseCell.textContent = item.name_purchase;
                row.appendChild(namePurchaseCell);

                let dateCell = document.createElement('td');
                dateCell.setAttribute('data-date', item.date);
                dateCell.textContent = item.date;
                row.appendChild(dateCell);

                let priceCell = document.createElement('td');
                priceCell.setAttribute('data-price', item.price);
                priceCell.textContent = item.price;
                row.appendChild(priceCell);

                let payerNumberCell = document.createElement('td');
                payerNumberCell.setAttribute('data-payer-number', item.payer_number);
                payerNumberCell.textContent = item.payer_number;
                row.appendChild(payerNumberCell);

                table.row.add(row);
            });
            table.draw();
        }
    });
});

});






