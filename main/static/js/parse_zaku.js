$(document).ready(function() {


  let table = $('#table-zaku').DataTable({
    "pageLength": 100,
    "order": [[0, 'asc']],
    "ordering": true,
    columns: [
        {title: "Keyword"},
        {title: "Ссылка"},
        {title: "Имя компании"},
        {title: 'УНП'},
        {title: "Предмет"},
        {title: "Предмет 2"},
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
            text: 'Завершить',
            className: 'button-table',
            action: function (e, dt, node, config){

                let selectedIds = [];
                let selectedRows = dt.rows({selected: true}).nodes();
                selectedRows.each(function(row) {
                    let tdElement = row.querySelector('td[data-id_purchase]');
                    let rowId = tdElement.getAttribute('data-id_purchase');
                    selectedIds.push(rowId);
                });
                completeFunction(selectedIds);

            }
        },
        {
            text: 'Удалить всё',
            className: 'button-table',
            action: function (e, dt, node, config){
                deleteAllFunction();
            }
        },
        {
            text: 'Старт',
            className: 'button-table-start',
            action: function (e, dt, node, config){
                start();
            }
        },
    ]
});

function completeFunction(id_list){
   $.ajax({
        url: "/complete_zaku/",
        type: "POST",
        data: {
            id_list: id_list,
        },
        dataType: "json",
        success: function(response) {
            let tableZaku = $('#table-zaku').DataTable();
            tableZaku.clear();
            console.log(response);
            response.parser_zaku.forEach(function(item) {
                let row = document.createElement('tr');

                let keywordCell = document.createElement('td');
                keywordCell.setAttribute('data-keyword', item.keyword);
                keywordCell.textContent = item.keyword;
                row.appendChild(keywordCell);

                let idPurchaseCell = document.createElement('td');
                idPurchaseCell.setAttribute('data-id_purchase', item.url);
                idPurchaseCell.textContent = item.url;
                row.appendChild(idPurchaseCell);

                let nameCompanyCell = document.createElement('td');
                nameCompanyCell.setAttribute('data-name_company', item.name_company);
                nameCompanyCell.textContent = item.name_company;
                row.appendChild(nameCompanyCell);

                let payerNumberCell = document.createElement('td');
                payerNumberCell.setAttribute('data-payer_number', item.payer_number);
                payerNumberCell.textContent = item.payer_number;
                row.appendChild(payerNumberCell);

                let mainNamePurchaseCell = document.createElement('td');
                mainNamePurchaseCell.setAttribute('data-main_name_purchase', item.main_name_purchase);
                mainNamePurchaseCell.textContent = item.main_name_purchase;
                row.appendChild(mainNamePurchaseCell);

                let namePurchaseCell = document.createElement('td');
                namePurchaseCell.setAttribute('data-name_purchase', item.name_purchase);
                namePurchaseCell.textContent = item.name_purchase;
                row.appendChild(namePurchaseCell);

                let priceCell = document.createElement('td');
                priceCell.setAttribute('data-price', item.price);
                priceCell.textContent = item.price;
                row.appendChild(priceCell);

                tableZaku.row.add(row);
            });
            tableZaku.draw();
        }
    });
}

function deleteAllFunction() {
    $.ajax({
        url: "/delete_all_zaku/",
        type: "GET",
        dataType: "json",
        success: function(response) {
            table.clear();
            table.draw();
        }
    });
}


function start(){
    $.ajax({
        url: "/data_zaku/",
        type: "POST",
        dataType: "json",
        success: function(response) {
            let tableZaku = $('#table-zaku').DataTable();
            tableZaku.clear();
            response.parser_zaku.forEach(function(item) {
                let row = document.createElement('tr');

                let keywordCell = document.createElement('td');
                keywordCell.setAttribute('data-keyword', item.keyword);
                keywordCell.textContent = item.keyword;
                row.appendChild(keywordCell);

                let idPurchaseCell = document.createElement('td');
                idPurchaseCell.setAttribute('data-id_purchase', item.url);
                idPurchaseCell.textContent = item.url;
                row.appendChild(idPurchaseCell);

                let nameCompanyCell = document.createElement('td');
                nameCompanyCell.setAttribute('data-name_company', item.name_company);
                nameCompanyCell.textContent = item.name_company;
                row.appendChild(nameCompanyCell);

                let payerNumberCell = document.createElement('td');
                payerNumberCell.setAttribute('data-payer_number', item.payer_number);
                payerNumberCell.textContent = item.payer_number;
                row.appendChild(payerNumberCell);

                let mainNamePurchaseCell = document.createElement('td');
                mainNamePurchaseCell.setAttribute('data-main_name_purchase', item.main_name_purchase);
                mainNamePurchaseCell.textContent = item.main_name_purchase;
                row.appendChild(mainNamePurchaseCell);

                let namePurchaseCell = document.createElement('td');
                namePurchaseCell.setAttribute('data-name_purchase', item.name_purchase);
                namePurchaseCell.textContent = item.name_purchase;
                row.appendChild(namePurchaseCell);

                let priceCell = document.createElement('td');
                priceCell.setAttribute('data-price', item.price);
                priceCell.textContent = item.price;
                row.appendChild(priceCell);

                tableZaku.row.add(row);
            });
            tableZaku.draw();
        }
    });
}

});
