// create_user file Validation

function valid()
{   
    const phoneData = document.getElementById('userInputPhone').value;

    if(phoneData.length>10 || phoneData.length<10){
        console.log('Contact No.:', phoneData)
        console.log('Length of Phone No:', phoneData.length)
        alert('Phone No should be of 10 digits. Pls enter Correct No!!')
        return false;
    }
    else{
        return true;
    }
    
}

//index file Validation

const gstCompany = document.getElementById('userCompanyGSTApply')
const quotationNo = document.getElementById('userQuotationNo')
// const paymentTerms = document.getElementById('userCompanyPayment')

gstCompany.addEventListener('input', ()=>{
    gstCompanyValue = gstCompany.value;
    if(isNaN(gstCompanyValue)){
        alert('Pls enter number!!')
        gstCompany.value = '';
    }
    else if(gstCompanyValue.length>2){
        alert('Pls enter correct GST No.!!')
        gstCompany.value = gstCompany.value.slice(0, 2);
    }
    else{
        false
    }
})

quotationNo.addEventListener('input', ()=>{
    quotation = quotationNo.value;
    if(isNaN(quotation)){
        alert('Pls enter Correct QuotationNo!!')
        quotationNo.value = '';
    }
})

// paymentTerms.addEventListener('input', ()=>{
//     paymentTermsValue = paymentTerms.value
//     if(/[0-9]/.test(paymentTermsValue)){
//         alert('Terms should not be in numbers')
//         paymentTerms.value = '';
//     }
// })