document.getElementById('userQuotationNo').addEventListener('focus', function () {
    const messageSpan = document.getElementById('lastQuotationMessage');

    // Fetch the last entered quotation number
    fetch('/getLastQuotation/')
        .then(response => response.json())
        .then(data => {
            if (data.lastQuotation) {
                messageSpan.textContent = `Last entered quotation number: ${data.lastQuotation}`;
                messageSpan.style.display = 'inline';
            } else {
                messageSpan.textContent = 'No quotations have been entered yet.';
                messageSpan.style.display = 'inline';
            }
        })
        .catch(error => {
            console.error('Error fetching last quotation number:', error);
        });
});

// Hide the message when the user leaves the field
document.getElementById('userQuotationNo').addEventListener('blur', function () {
    const messageSpan = document.getElementById('lastQuotationMessage');
    messageSpan.style.display = 'none';
});
