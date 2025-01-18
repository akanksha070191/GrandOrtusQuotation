// Create a new row
var newRow = table.insertRow();
var newAMCRow = amc_table.insertRow();
var newSubscriptionRow = subscription_table.insertRow();


// Insert new cells for each column
var cell1 = newRow.insertCell(0);
var cell2 = newRow.insertCell(1);
var cell3 = newRow.insertCell(2);
var cell4 = newRow.insertCell(3);
var cell5 = newRow.insertCell(4);
var cell6 = newRow.insertCell(5);
var cell7 = newRow.insertCell(6);

// Add input fields into the new cells
cell1.innerHTML = '<input type="text" name="item_name[]" placeholder="item name">';
cell2.innerHTML = '<textarea name="item_description[]"  placeholder="item description"></textarea>'
cell3.innerHTML = '<input type="number" name="warrenty_year[]" placeholder="year of warrenty">';
cell4.innerHTML = '<input type="number" name="units[]" placeholder="units">';
cell5.innerHTML = '<input type="number" name="price[]" placeholder="price">';
cell6.innerHTML = '<input type="number" name="margin[]" placeholder="margin">';
cell7.innerHTML = '<button class="button-style" onclick="deleteRow(this)">Delete</button>';

// Insert new cells for each column in AMC Table
var cell11 = newAMCRow.insertCell(0);
var cell12 = newAMCRow.insertCell(1);
var cell13 = newAMCRow.insertCell(2);
var cell14 = newAMCRow.insertCell(3);
var cell15 = newAMCRow.insertCell(4);
var cell16 = newAMCRow.insertCell(5);
var cell17 = newAMCRow.insertCell(6);
var cell18 = newAMCRow.insertCell(7);
var cell19 = newAMCRow.insertCell(8);
var cell20 = newAMCRow.insertCell(9);

// Add input fields into the new cells in AMC Table
cell11.innerHTML = '<input type="text" name="item_name[]" placeholder="item name">';
cell12.innerHTML = '<textarea name="item_description[]"  placeholder="item description"></textarea>'
cell13.innerHTML = '<input type="number" name="amc_year[]" placeholder="amc-time">';
cell14.innerHTML = '<input type="number" name="hsn/sac[]" placeholder="hsn/sac">';
cell15.innerHTML = '<input type="date" name="start_date[]" placeholder="start-date">';
cell16.innerHTML = '<input type="date" name="end_date[]" placeholder="end-date">'
cell17.innerHTML = '<input type="number" name="units[]" placeholder="units">';
cell18.innerHTML = '<input type="number" name="price[]" placeholder="price">';
cell19.innerHTML = '<input type="number" name="margin[]" placeholder="margin">';
cell20.innerHTML = '<button class="button-style" onclick="deleteRow(this)">Delete</button>';

// Insert new cells for each column in Subscription Table
var cell21 = newSubscriptionRow.insertCell(0);
var cell22 = newSubscriptionRow.insertCell(1);
var cell23 = newSubscriptionRow.insertCell(2);
var cell24 = newSubscriptionRow.insertCell(3);
var cell25 = newSubscriptionRow.insertCell(4);
var cell26 = newSubscriptionRow.insertCell(5);
var cell27 = newSubscriptionRow.insertCell(6);
var cell28 = newSubscriptionRow.insertCell(7);
var cell29 = newSubscriptionRow.insertCell(8);


// Add input fields into the new cells in Subscription Table
cell21.innerHTML = '<input type="text" name="item_name[]" placeholder="item name">';
cell22.innerHTML = '<textarea name="item_description[]"  placeholder="item description"></textarea>';
cell23.innerHTML = '<input type="number" name="subscription_year[]" placeholder="subscription-time">';
cell24.innerHTML = '<input type="date" name="start_date[]" placeholder="start-date">';
cell25.innerHTML = '<input type="date" name="end_date[]" placeholder="end-date">'
cell26.innerHTML = '<input type="number" name="units[]" placeholder="units">';
cell27.innerHTML = '<input type="number" name="price[]" placeholder="price">';
cell28.innerHTML = '<input type="number" name="margin[]" placeholder="margin">';
cell29.innerHTML = '<button class="button-style" onclick="deleteRow(this)">Delete</button>';


//get table body content

var table = document.getElementById('quotationTable').getElementsByTagName('tbody')[0];
    var amc_table = document.getElementById('amcQuotationTable').getElementsByTagName('tbody')[0];
    var subscription_table = document.getElementById('subscriptionQuotationTable').getElementsByTagName('tbody')[0];

