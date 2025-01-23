document.addEventListener("DOMContentLoaded", function () {
    initializeSignaturePad();
});
function initializeSignaturePad(){
    const canvas = document.getElementById('signature-pad');
    const signaturePad = new SignaturePad(canvas);
    function resizeCanvas() {
        var ratio = Math.max(window.devicePixelRatio || 1, 1);
        // Set canvas size to match its CSS styling and apply the device pixel ratio
        canvas.width = canvas.offsetWidth * ratio;
        canvas.height = canvas.offsetHeight * ratio;
        canvas.getContext("2d").scale(ratio, ratio);
    }

    // Resize canvas when the window is resized
    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    window.clearSignature = function(){
            signaturePad.clear();
            document.getElementById('signature-data').value = '';
            document.getElementById('signature-image').src = '';
        };

    window.saveSignature = function(){
        if (signaturePad.isEmpty()){
                alert("Signature Required")
            }
        else{
                var signatureData = signaturePad.toDataURL();
                document.getElementById('signature-data').value = signatureData;
                document.getElementById('signature-image').src = signatureData;
                alert("Signature saved!");
            }
    }

}
document.addEventListener("DOMContentLoaded", initializeSignaturePad);


const existingRows = [];
const columnOrder = ['itemName', 'itemDescription', 'hsnsac', 'productSlNo', 'partNo', 'orderID', 'partID', 'contractID', 'instane', 'amc', 'warrenty', 'subscription', 'startDate', 'endDate', 'units', 'lot', 'unitPrice', 'margin'];
const selectedColumns = new Set();
let rowCount = 0;


document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        const columnClass = this.value;
        console.log('columnClass Name:', columnClass)
        const columnIndex = columnOrder.indexOf(columnClass);
        console.log("column index:", columnIndex)
        const elements = document.querySelectorAll('.' + columnClass);
        console.log('ElementName', elements)
        

        // Show/Hide the columns based on checkbox state
        if (this.checked) {
            selectedColumns.add(columnClass)
            elements.forEach(el => el.style.display = 'table-cell');
            existingRows.forEach((row, index) => {
                if(!row.querySelector('.'+columnClass)){
                    const newCell = document.createElement('td');
                    newCell.classList.add(columnClass, 'column');

                    const input = document.createElement('input');
                    input.type = 'text';
                    input.name = columnClass + '[]';
                    input.placeholder = columnClass + "(Row" + (index+1) + ")";
                    newCell.appendChild(input);

                    row.insertBefore(newCell, row.children[columnIndex]);
                    newCell.style.display = 'table-cell';
                    
                }
            });
        } else {
            selectedColumns.delete(columnClass);
            elements.forEach(el => el.style.display = 'none');
        }

    });
});

document.getElementById('addRowBtn').addEventListener('click', function() {
    rowCount++;
    const selectedColumns = [];

    document.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox =>{
        selectedColumns.push(checkbox.value);
    });

    const tableBody = document.getElementById('boqFormTableBody');
    const newBOQRow = document.createElement('tr');

    columnOrder.forEach((column, columnIndex) => {
    
        const cell = document.createElement('td');
        cell.classList.add(column, 'column');

        if (selectedColumns.includes(column)) {
            const input = document.createElement('input');
            input.type = 'text';
            input.name = column + '[]';
            if(column === 'startDate' || column === 'endDate'){
                
                input.placeholder = "YYYY-MM-DD"; 
                cell.appendChild(input);
                cell.style.display = 'table-cell'; // Show the column
                input.addEventListener('blur', ()=>{
                    if(!validateDateFormat(input.value)){
                        input.value = '';
                    }
                });

            }
            else{
                input.placeholder = column; // Placeholder for easier identification
                cell.appendChild(input);
                cell.style.display = 'table-cell'; // Show the column
            }
            
        } else {
            cell.style.display = 'none'; // Keep it hidden if not selected
        }
    
        newBOQRow.appendChild(cell);
        });
        tableBody.appendChild(newBOQRow);
        existingRows.push(newBOQRow);

    
});

function validateDateFormat(dateString) {
    const date = new Date(dateString);
    const [year, month, day] = dateString.split('-');

    // Check if the dateString is in the YYYY-MM-DD format and if it's a valid date
    if (
        date instanceof Date &&
        !isNaN(date) &&
        date.getFullYear() == year &&
        date.getMonth() + 1 == month &&
        date.getDate() == day
    ) {
        return true;
    } else {
        alert("Invalid date format. Please enter the date as YYYY-MM-DD.");
        return false;
    }
}


// const quotationtype = document.getElementById('userCompanyQuotation');
// const warrentyForm = document.getElementById('warrentyForm');
// const amcForm = document.getElementById('amcForm');
// const subscriptionForm = document.getElementById('subscriptionForm')
// const checkboxDisplayForm = document.getElementById('checkboxDisplay');
// const boqForm = document.getElementById('boqForm');
// const footerData = document.getElementById('footerData');


// quotationtype.addEventListener("change", function(){
//     footerData.style.display = "none";
//     warrentyForm.style.display = "none";
//     amcForm.style.display = "none";
//     subscriptionForm.style.display = "none";
//     checkboxDisplayForm.style.display = "none";
//     boqForm.style.display = "none";
//     if(this.value === 'Warrenty/Supply'){
//         warrentyForm.style.display = "block";
//         footerData.style.display = "block";
//     }
//     else if(this.value === 'AMC Support'){
//         amcForm.style.display = "block";
//         footerData.style.display = "block";
//     }
//     else if(this.value === 'Subscription/Licence'){
//         subscriptionForm.style.display = "block";
//         footerData.style.display = "block";
//     }
//     else if(this.value === 'BOQ'){
//         checkboxDisplayForm.style.display = "block";
//         boqForm.style.display = "block";
//         footerData.style.display = "block";
//     }
// });

document.getElementById('clearCheckboxBox').addEventListener('click', function(){
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    console.log(checkboxes)
    checkboxes.forEach(checkbox => {
            checkbox.checked = false;
            selectedColumns.clear();
            columnOrder.forEach(columnClass => {
                const elements = document.querySelectorAll('.' + columnClass);
                elements.forEach(el => el.style.display = 'none'); // Hide all columns and data
                document.getElementById('boqFormTableBody').innerHTML = '';
                // existingRows = [];
                rowCount = 0;
            });
        
    });
});


let clientNames = [];
fetchData();
async function fetchData(){
    const response = await fetch(`/api/getCompanyInfo/`);
    if(!response.ok){
        console.log('Data not correct')
    }
    const data = await response.json();
    clientNames = data.rows.map((client)=>{
        return client.clientName
    })
}

let activeCompanyNameField = null;

function onInputEnter(){
    removeAutoCompleteDropdown();
    clearCompanyDetails();

    if (!activeCompanyNameField) return;

    const value = activeCompanyNameField.value.toLowerCase();
    // const value = document.getElementById('userInputCompanyName').value.toLowerCase();
    // const value2 = document.getElementById('user2InputCompanyName').value.toLowerCase();
    
    if (value.length === 0) return;

    const filteredClientName = [];
    clientNames.forEach((name)=>{
        if(name.substring(0, value.length).toLowerCase() === value)
            filteredClientName.push(name);
            
    });
    console.log(filteredClientName);
    createAutoCompleteDropdown(filteredClientName);
}

function clearCompanyDetails() {
    // Clear company address and GST fields
    document.getElementById('userCompanyGST').value = '';
    document.getElementById('userCompanyAddress').value = '';
    document.getElementById('user2CompanyGST').value = '';
    document.getElementById('user2CompanyAddress').value = '';
}



function createAutoCompleteDropdown(list){
    removeAutoCompleteDropdown();

    const listEl = document.createElement('ul');
    listEl.className = 'autocomplate-list';
    listEl.id = 'autocomplate-list';

    list.forEach((client)=>{
        const listItem = document.createElement('li');
        const clientButton = document.createElement('button');
    
        clientButton.innerHTML = client;
        clientButton.addEventListener("click", onUserInputClickButton)
        listItem.appendChild(clientButton);



        listEl.appendChild(listItem);
    });

    if(activeCompanyNameField){
        const parentWrapper = activeCompanyNameField.closest('.autocomplete-wrapper');
        parentWrapper.appendChild(listEl)
    }

}

function removeAutoCompleteDropdown(){
    const listEl = document.getElementById('autocomplate-list');

    if (listEl){
        listEl.remove();
    }
}

async function onUserInputClickButton(e){
    e.preventDefault();

    const buttonEl = e.target;
    if(!activeCompanyNameField) return;

    activeCompanyNameField.value = buttonEl.innerHTML;
    const clientName = activeCompanyNameField.value;

    // const inputValue = document.getElementById('userInputCompanyName');
    // const inputValue2 = document.getElementById('user2InputCompanyName');
    // inputValue.value = buttonEl.innerHTML;
    // inputValue2.value = buttonEl.innerHTML;
    // const clientName = inputValue.value;
    // const clientName2 = inputValue2.value;

    removeAutoCompleteDropdown();

    if (clientName){
        try{
            const response = await fetch(`/api/getClientData/?companyname=${encodeURIComponent(clientName)}`, {cache:'no-store'});
            if (!response.ok){
                throw new Error('Company not Found')
            }
            const data = await response.json();
            document.getElementById('userCompanyGST').value = data.clientGST || '';
            document.getElementById('userCompanyAddress').value = data.clientAddress || '';
            document.getElementById('user2CompanyGST').value = data.clientGST || '';
            document.getElementById('user2CompanyAddress').value = data.clientAddress || '';
        } catch (error){
            console.log('Error Fetching Company Data:', error);
            document.getElementById('userCompanyGST').value = '';
            document.getElementById('userCompanyAddress').value = '';
            document.getElementById('user2CompanyGST').value = '';
            document.getElementById('user2CompanyAddress').value = '';
        }
    }
}

function clearFormData(form){
    const inputs = form.querySelectorAll('input[type="text"]');
    inputs.forEach((input)=>{
        input.value = '';
    })
    
}


function enableAutocomplete(field){
    field.addEventListener("input", onInputEnter);
    activeCompanyNameField = field;
}

function disableAutocomplete(field){
    field.removeEventListener('input', onInputEnter);
    activeCompanyNameField = null;
}

const newQuotation = document.getElementById('optForNewQuotation');
const form = document.getElementById('form3Class');
const form4 = document.getElementById('form4Class');
console.log(newQuotation)
const formData = document.getElementById('formClass');
console.log(formData)
formData.style.display = 'none';

// form2Data.style.display = 'none';
newQuotation.addEventListener('click', ()=>{
    clearFormData(formData);
    formData.style.display = 'block';
    form2Data.style.display = 'none';
    form.style.display = 'none';
    form4.style.display = 'none';
    disableAutocomplete(document.getElementById('user2InputCompanyName')); 
    enableAutocomplete(document.getElementById('userInputCompanyName')); 
})

const reviseQuotation = document.getElementById('optForReviseQuotation');
const form2Data = document.getElementById('form2Class');

// formData.style.display = 'none';
form2Data.style.display = 'none';
reviseQuotation.addEventListener('click', ()=>{
    clearFormData(form2Data);
    form2Data.style.display = 'block';
    formData.style.display = 'none';
    form.style.display = 'none';
    form4.style.display = 'none';
    disableAutocomplete(document.getElementById('userInputCompanyName')); 
    enableAutocomplete(document.getElementById('user2InputCompanyName')); 
})



async function fetchQuotationDetails(){
    const quotationNo = document.getElementById('user2QuotationNo').value;
    const companyName = document.getElementById('user2InputCompanyName').value;
    console.log('company name:', companyName);
    console.log(quotationNo);
    if (quotationNo && companyName){
        try{
            const quotationResponce = await fetch(`reviseQuotationData/?quotationNo=${encodeURIComponent(quotationNo)}&companyName=${encodeURIComponent(companyName)}`)
            if(!quotationResponce.ok){
                throw new Error('Company not Found')
            }
            const quotationData = await quotationResponce.json();
            console.log(quotationData)
            console.log(typeof(quotationData))
            newUpdatedTable(quotationData)
        }
        catch(error){
            alert('Error Fetching Company Data Please Enter Correct Quotation No', error);
            console.log('Error Fetching Company Data:', error);
        }
    }else{
        alert('Please Enter Both Company Name and Quotation No');
    }

}

function newUpdatedTable(quotationDataNew){
    const quotationTable = document.getElementById('revisedQuotationTable');
    quotationTable.style.display = 'block';
    const quotationTableData = document.getElementById('revisedQuotationBody');
    // const array = Object.values(quotationDataNew);
    const array = Array.isArray(quotationDataNew) ? quotationDataNew : Object.values(quotationDataNew);

    array.forEach(row => {
        if (Array.isArray(row)){
            row.forEach(item =>{
                const tableRow = document.createElement("tr");
                console.log('item is:', item)

                tableRow.innerHTML = `
                <td>${item['ID'] || 'N/A'}</td>
                <td>${item['SL No.'] || 'N/A'}</td>
                <td>${item['Item Name'] || 'N/A'}</td>
                <td>${item['Item Description'] || 'N/A'}</td>
                <td>${item['Units'] || 'N/A'}</td>
                <td>${item['Cost Price'] || 'N/A'}</td>
                <td>${item['Old Margin'] || 'N/A'}</td>
                <td>${item['Price'] || 'N/A'}</td>
                <td contenteditable="true"></td>
                <td contenteditable="true"></td>
                <td>
                    <button class="delete-row-btn" onclick="deleteRow(this)">Delete</button>
                </td>
            `;
            quotationTableData.appendChild(tableRow);

                // const cell0 = document.createElement("td");
                // cell0.textContent = item['SL No.'] || 'N/A';
                // tableRow.appendChild(cell0);

                // const cell1 = document.createElement("td");
                // cell1.textContent = item['Item Name'] || 'N/A';
                // tableRow.appendChild(cell1);

                // const cell2 = document.createElement("td");
                // cell2.textContent = item['Item Description'] || 'N/A';
                // tableRow.appendChild(cell2);

                // const cell3 = document.createElement("td");
                // cell3.textContent = item['Units'] || 'N/A';
                // tableRow.appendChild(cell3);

                // const cell4 = document.createElement("td");
                // cell4.textContent = item['Cost Price'] || 'N/A';
                // tableRow.appendChild(cell4);

                // const cell5 = document.createElement("td");
                // cell5.textContent = item['Old Margin'] || 'N/A';
                // tableRow.appendChild(cell5);
                
                // const cell6 = document.createElement("td");
                // cell6.textContent = item['Price'] || 'N/A';
                // tableRow.appendChild(cell6);

                // const cell7 = document.createElement("td");
                // cell7.contentEditable = "true";
                // cell7.textContent = '';
                // tableRow.appendChild(cell7);

                // const cell8 = document.createElement("td");
                // cell8.contentEditable = "true";
                // cell8.textContent = '';
                // tableRow.appendChild(cell8);

                // quotationTableData.appendChild(tableRow);

            });
        } else {
                const tableRow = document.createElement("tr");

                tableRow.innerHTML = `
                <td>${item['ID'] || 'N/A'}</td>
                <td>${item['SL No.'] || 'N/A'}</td>
                <td>${item['Item Name'] || 'N/A'}</td>
                <td>${item['Item Description'] || 'N/A'}</td>
                <td>${item['Units'] || 'N/A'}</td>
                <td>${item['Cost Price'] || 'N/A'}</td>
                <td>${item['Old Margin'] || 'N/A'}</td>
                <td>${item['Price'] || 'N/A'}</td>
                <td contenteditable="true"></td>
                <td contenteditable="true"></td>
                <td>
                    <button class="delete-row-btn" onclick="deleteRow(this)">Delete</button>
                </td>
            `;
            quotationTableData.appendChild(tableRow);

                // const cell0 = document.createElement("td");
                // cell0.textContent = item['SL No.'] || 'N/A';
                // tableRow.appendChild(cell0);

                // const cell1 = document.createElement("td");
                // cell1.textContent = item['Item Name'] || 'N/A';
                // tableRow.appendChild(cell1);

                // const cell2 = document.createElement("td");
                // cell2.textContent = item['Item Description'] || 'N/A';
                // tableRow.appendChild(cell2);

                // const cell3 = document.createElement("td");
                // cell3.textContent = item['Units'] || 'N/A';
                // tableRow.appendChild(cell3);

                // const cell4 = document.createElement("td");
                // cell4.textContent = item['Cost Price'] || 'N/A';
                // tableRow.appendChild(cell4);

                // const cell5 = document.createElement("td");
                // cell5.textContent = item['Old Margin'] || 'N/A';
                // tableRow.appendChild(cell5);
                
                // const cell6 = document.createElement("td");
                // cell6.textContent = item['Price'] || 'N/A';
                // tableRow.appendChild(cell6);

                // const cell7 = document.createElement("td");
                // cell7.contentEditable = "true";
                // cell7.textContent = '';
                // tableRow.appendChild(cell7);

                // const cell8 = document.createElement("td");
                // cell8.contentEditable = "true";
                // cell8.textContent = '';
                // tableRow.appendChild(cell8);

                // quotationTableData.appendChild(tableRow);

        }

        
    });
}

let deletedRows = []; // Array to store IDs of deleted rows

function deleteRow(button) {
    const row = button.closest('tr'); // Get the row
    const id = row.querySelector('td').textContent; // Get the unique SL No.
    deletedRows.push(id); // Add SL No. to deletedRows array
    row.remove(); // Remove the row from the table
}


document.getElementById('user2QuotationNo').addEventListener("input", fetchQuotationDetails);

function getTableData(event){
    event.preventDefault();
    console.log("Button clicked");
    const tableRows = document.querySelectorAll('#revisedQuotationBody tr' );
    const tabledata = [];
    const quotationNo = document.getElementById('user2QuotationNo').value;
    tableRows.forEach(row =>{
        const cells = row.querySelectorAll('td');
        const newMargin = cells[8].textContent;
        const newPrice = cells[9].textContent;
         tabledata.push({
            ID: cells[0].textContent,
            SLNo: cells[1].textContent,
            itemName: cells[2].textContent,
            itemDescription: cells[3].textContent,
            units: cells[4].textContent,
            costPrice: cells[5].textContent,
            oldMargin: cells[6].textContent,
            price: cells[7].textContent,

            newMargin: newMargin, 
            newPrice: newPrice,  
         });
         console.log('Table Data:', tabledata);
         console.log('New Margin:', newMargin);
         console.log('New Price:', newPrice);
    });
    sendTableDataToServer(tabledata, quotationNo)
}

function sendTableDataToServer(tabledata, quotationNo){
    fetch('/generateReviseQuotation/',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ tabledata: tabledata, quotationNo:quotationNo, deletedRows: deletedRows})
    })

    .then(response => {
        return response.text();  // Read response as text
    })
    .then(text => {
        // console.log('Response Body:', text);  // Log the response body
        try {
            const data = JSON.parse(text); // Try to parse as JSON
            console.log('Parsed JSON:', data);
            // Handle the JSON data here if it's valid
        } catch (error) {
            console.error('Error parsing JSON:', error);
            // Optionally display the HTML response to debug
            document.open();
            document.write(text); // Display the HTML response
            document.close();
        }
        if (typeof SignaturePad === 'undefined') {
            const script = document.createElement('script');
            script.src = "https://cdn.jsdelivr.net/npm/signature_pad@4.0.0/dist/signature_pad.umd.min.js";
            script.onload = initializeSignaturePad;
            document.head.appendChild(script);
        } else {
            initializeSignaturePad();
        }
    })
    .catch(error => { 
        console.error('Error:', error);
    });    
}
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return '';
}
document.addEventListener("DOMContentLoaded", initializeSignaturePad);
// document.getElementById('generateReviseQuotationButton').addEventListener("click", getTableData);