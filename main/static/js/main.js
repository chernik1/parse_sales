
$(document).ready(function() {

    document.getElementById('start-button').addEventListener('click', function() {
    $.ajax({
        url: 'data/',
        type: 'GET',
        success: function(response) {
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

                $('#table').append(row);
            });
        },
    });
});


    let table;
    table = $('#table').DataTable({
        "pageLength": 100,
        "order": [[0, 'asc']],
        "ordering": true,
        columns: [
            {title: "Keyword"},
            {title: "Регистрационный номер"},
            {title: "Имя компании"},
            {title: "Предмет"},
            {title: "Дата"},
            {title: "Цена"},
            {title: 'УНП'},
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
                className: 'button-table',
                action: function (e, dt, node, config) {
                    let selectedIds = [];
                    let selectedRows = dt.rows({selected: true}).nodes();
                    selectedRows.each(function(row) {
                        let tdElement = row.querySelector('td[data-id_purchase]');
                        let rowId = tdElement.getAttribute('data-id_purchase');
                        selectedIds.push(rowId);
                    });
                deleteFunction(selectedIds);
            }
        }],
    });
});

function deleteFunction(id_list) {
    $.ajax({
        url: "/delete/",
        type: "POST",
        data: {
            id_list: id_list,
        },
        dataType: "json",
        success: function(response) {
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

                $('#table').append(row);
            });
        }
    });
}

