document.addEventListener('DOMContentLoaded', function () {
    const deleteButton = document.getElementById('deleteQuotation');
    const form = document.getElementById('form3Class');
    const form1 = document.getElementById('formClass');
    const form2= document.getElementById('form2Class');
    const form4 = document.getElementById('form4Class');
    deleteButton.addEventListener('click', function () {
        // Toggle the display property of the form
        if (form4.style.display === 'none') {
            form4.style.display = 'block'; // Show the form
            form1.style.display = 'none';
            form2.style.display = 'none';
            form.style.display = 'none';
        } else {
            form4.style.display = 'none'; // Hide the form (optional, for toggling behavior)
        }
    });
});