document.addEventListener('DOMContentLoaded', function () {
    const askPrice = document.getElementById('askPrice');
    const form = document.getElementById('form3Class');
    const form1 = document.getElementById('formClass');
    const form2= document.getElementById('form2Class');
    const form4 = document.getElementById('form4Class');
    const form5 = document.getElementById('form5Class');
    askPrice.addEventListener('click', function () {
        // Toggle the display property of the form
        if (form5.style.display === 'none') {
            form5.style.display = 'block'; // Show the form
            form1.style.display = 'none';
            form2.style.display = 'none';
            form.style.display = 'none';
            form4.style.display = 'none';
        } else {
            form5.style.display = 'none'; // Hide the form (optional, for toggling behavior)
        }
    });
});

document.getElementById('clearProductCheckbox').addEventListener('click', function(){
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    console.log(checkboxes)
    checkboxes.forEach(checkbox => {
            checkbox.checked = false;
            selectedColumns.clear();
            // columnOrder.forEach(columnClass => {
            //     const elements = document.querySelectorAll('.' + columnClass);
            //     elements.forEach(el => el.style.display = 'none'); // Hide all columns and data
                // document.getElementById('boqFormTableBody').innerHTML = '';
                // existingRows = [];
                // rowCount = 0;
            // });
        
    });
});
