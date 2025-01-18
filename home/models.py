from django.db import models

# Create your models here.

class LogInUser(models.Model):
    firstName = models.CharField(max_length=250)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phoneNumber = models.CharField(max_length=15)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.firstName}"

class CompanyDetails(models.Model):
    companyName = models.CharField(max_length=250)
    companyAddress = models.CharField(max_length=500)
    companyPayment = models.CharField(max_length=50)
    companyGST = models.CharField(max_length=50, primary_key=True)
    quotationFor = models.CharField(max_length=200)
    quotationType = models.CharField(max_length=200, null=True)
    priceValidTill = models.CharField(max_length=100, null=True)
    paymentTerms = models.CharField(max_length=100, null=True)
    gstApply = models.CharField(max_length=100, null=True)
    deliveryTime = models.CharField(max_length=500,null=True)
    importantNote = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f"{self.companyName}"
    
    
class clientDetails(models.Model):
    ID = models.AutoField(primary_key=True)
    clientName = models.CharField(max_length=255)
    Address = models.CharField(max_length=255, null=True)
    GSTDetails = models.CharField(max_length=255, null=True)
    concernPersonName = models.CharField(max_length=255, null=True)
    Designation = models.CharField(max_length=255, null=True)
    emailID = models.CharField(max_length=255, null=True)
    phoneNo = models.CharField(max_length=255, null=True)

    class Meta:
        managed = False  # Prevent Django from trying to create/update this table
        db_table = 'clientDetails'  # The name of the existing table in the database

class QuotationTable(models.Model):
    itemName = models.TextField()
    itemDescription = models.CharField(max_length=500)
    warrentyYear = models.IntegerField(null=True)
    units = models.IntegerField()
    price = models.IntegerField()
    margin = models.IntegerField()
    companyGST = models.ForeignKey("CompanyDetails", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemName}"
    
class BOQQuotationTable(models.Model):
    itemName = models.TextField()
    itemDescription = models.CharField(max_length=500)
    hsn_sac = models.CharField(max_length=50, null=True)
    productSlNo = models.CharField(max_length=20, null=True)
    quotationType = models.CharField(max_length=20, null=True)
    quotationNo = models.CharField(max_length=50, null=True)
    partNo = models.CharField(max_length=100, null=True)
    orderId = models.CharField(max_length=100, null=True)
    partId = models.CharField(max_length=100, null=True)
    warrentyYear = models.CharField(max_length=20, null=True)
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    instane = models.CharField(max_length=20, null=True)
    contractId = models.CharField(max_length=20, null=True)
    units = models.IntegerField()
    lots = models.IntegerField(null=True, blank=True)
    price = models.CharField(max_length=50)
    margin = models.IntegerField()
    totalUnitPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=0.00)
    totalAmount = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=0.00)
    currentDate = models.DateField(null=True)
    newMargin = models.FloatField(null=True)
    newMarginAppliedPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=0.00)
    newMarginPrice = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=0.00)
    companyGST = models.ForeignKey("CompanyDetails", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.itemName}"
    
