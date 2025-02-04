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

document.getElementById('clearProductDropdown').addEventListener('click', function () {
    // Get the dropdown element
    const productDropdown = document.getElementById('productDropdown');

    // Deselect all options in the dropdown
    Array.from(productDropdown.options).forEach(option => (option.selected = false));

    // Clear the product list input field
    document.getElementById('productList').value = '';

    // Clear the vendor list
    const vendorList = document.getElementById('vendors');
    vendorList.innerHTML = '<li>No vendors selected</li>';

    // Clear the vendor mail list input field
    document.getElementById('vendorMailList').value = '';
});


document.addEventListener('DOMContentLoaded', function () {
    const productDropdown = document.getElementById('productDropdown');
    const vendorList = document.getElementById('vendors');

    // Update productList input on selection change
    productDropdown.addEventListener('change', function () {
        const selectedOptions = Array.from(productDropdown.selectedOptions).map(option => option.value);
        document.getElementById('productList').value = selectedOptions.join(', ');

        // Fetch vendors for selected products
        fetch('/fetchVendors/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ products: selectedOptions }),
        })
        .then(response => response.json())
        .then(data => {
            vendorList.innerHTML = ''; // Clear existing vendors

            if (data.vendors.length > 0) {
                data.vendors.forEach(vendor => {
                    const label = document.createElement('label');
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.value = vendor.emailID;

                    label.appendChild(checkbox);
                    label.appendChild(document.createTextNode(` ${vendor.vendorName} - ${vendor.emailID}`));

                    // Add event listener for email selection
                    checkbox.addEventListener('change', function () {
                        const selectedEmails = Array.from(vendorList.querySelectorAll('input[type="checkbox"]:checked'))
                            .map(cb => cb.value);
                        document.getElementById('vendorMailList').value = selectedEmails.join(', ');
                    });

                    vendorList.appendChild(label);
                });
            } else {
                vendorList.innerHTML = '<li>No vendors found</li>';
            }
        })
        .catch(error => console.error('Error fetching vendors:', error));
    });

    // Clear product dropdown selection
    document.getElementById('clearProductDropdown').addEventListener('click', function () {
        Array.from(productDropdown.options).forEach(option => (option.selected = false));
        document.getElementById('productList').value = ''; // Clear product list input
    });
});

function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                cookieValue = decodeURIComponent(cookie.substring('csrftoken='.length));
                break;
            }
        }
    }
    return cookieValue;
}