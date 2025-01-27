from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,logout, login
# from django.contrib.auth.models import User
from django.contrib import messages
from .models import LogInUser, BOQQuotationTable, CompanyDetails, clientDetails
from django.http import HttpResponse, JsonResponse
from datetime import datetime
import json
from django.db import connection
from collections import defaultdict
import re
from decimal import Decimal
from django.core.cache import cache
from django.views.decorators.cache import cache_control


# Create your views here.


def index(request):
    username = request.session.get('username', None)
    print("heelo in index()")
    if username is not None:
        return render(request, 'index.html', {'username':username})
    else:
        return render(request, 'login.html')

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        userdata = LogInUser.objects.values('firstName', 'password')
        print(userdata)
        for data in userdata:
            print(data)
            if username == data['firstName'] and password == data['password']:
                request.session['username'] = username
                return redirect('/')
        messages.error(request, "Wrong username or password. Try Again!!")
        return render(request, 'login.html')
    return render(request, 'login.html')

def logoutUser(request):
    print(request.session['username'])
    if 'username' in request.session:
        print(request.session['username'])
        request.session.flush()
        print('hii')
    request.session.modified = True  # Ensure session is updated
    logout(request)
    return redirect('login')

def createNewUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = LogInUser(firstName=username, lastName=lname, email=email, phoneNumber=phone, password=password)
        user.save()
        messages.success(request, 'Account Created.. Pls LogIn!!')
        return redirect('create_user')
    else:
        return render(request, 'create_user.html')
    
def generate_quotation(request):
    if request.method == 'POST':
        companyName = request.POST.get('companyname')
        companyAddress = request.POST.get('address')
        companyGST = request.POST.get('companygst')
        companyGSTApply = request.POST.get('companygstapply')
        companyQuotationNo = request.POST.get('quotationNo')
        companyPayment = request.POST.get('paymentterms')
        quotationFor = request.POST.get('quotationfor')
        pricevalidtill = request.POST.get('pricevalidtill')
        deliveryTime = request.POST.get('deliveryTime')
        importantNote = request.POST.get('importantNote')
        quotationType = request.POST.get('quotationtype')
        itemName = request.POST.getlist('itemName[]')
        itemDescription = request.POST.getlist('itemDescription[]')
        hsn_sac = request.POST.getlist('hsnsac[]')
        productSlNo = request.POST.getlist('productSlNo[]')
        partNo = request.POST.getlist('partNo[]')
        orderId = request.POST.getlist('orderID[]')
        partId = request.POST.getlist('partID[]')
        startDate = request.POST.getlist('startDate[]')
        endDate = request.POST.getlist('endDate[]')
        instane = request.POST.getlist('instane[]')
        contractId = request.POST.getlist('contractID[]')
        warrentyYear = request.POST.getlist('warrenty[]')
        units = request.POST.getlist('units[]')
        lots = request.POST.getlist('lot[]')
        price = request.POST.getlist('unitPrice[]')
        margin = request.POST.getlist('margin[]')

        
        financialYearStart = str(datetime.now().year)[2:]
        # print(financialYearStart, type(financialYearStart))
        financialYearEnd = int(financialYearStart) + 1
        companyQuotationNoFinal = 'GOSPL/Q/'+financialYearStart+'-'+str(financialYearEnd)+'/'+companyQuotationNo
        
        companyDetails = CompanyDetails(companyName=companyName, companyAddress=companyAddress, companyPayment=companyPayment, companyGST=companyGST, quotationFor=quotationFor, quotationType=quotationType, priceValidTill=pricevalidtill, paymentTerms=companyPayment, gstApply=companyGSTApply, deliveryTime=deliveryTime, importantNote=importantNote)
        companyDetails.save()

        companyGSTRetrieve = CompanyDetails.objects.get(companyGST=companyGST)

        max_length = max(len(itemName), len(itemDescription), len(hsn_sac), len(productSlNo), len(partNo), len(orderId), len(partId), len(startDate), len(endDate), len(instane), len(contractId), len(warrentyYear), len(units), len(lots), len(price), len(margin))

        # Ensure all lists are of the same length by padding with empty strings or None
        itemName.extend([''] * (max_length - len(itemName)))
        itemDescription.extend([''] * (max_length - len(itemDescription)))
        hsn_sac.extend([''] * (max_length - len(hsn_sac)))
        productSlNo.extend([''] * (max_length - len(productSlNo)))
        partNo.extend([''] * (max_length - len(partNo)))
        orderId.extend([''] * (max_length - len(orderId)))
        partId.extend([''] * (max_length - len(partId)))
        startDate.extend([''] * (max_length - len(startDate)))
        endDate.extend([''] * (max_length - len(endDate)))
        instane.extend([''] * (max_length - len(instane)))
        contractId.extend([''] * (max_length - len(contractId)))
        warrentyYear.extend([''] * (max_length - len(warrentyYear)))
        units.extend([''] * (max_length - len(units)))
        lots.extend([''] * (max_length - len(lots)))
        price.extend([''] * (max_length - len(price)))
        margin.extend([''] * (max_length - len(margin)))

        totalAmountValue = []
        unitPriceValueList = []

        print('lots', lots)
        print('quotationtype: ', quotationType)

        if quotationType == 'Subscription/Lisence':
            tableData = zip(itemName, itemDescription, hsn_sac, productSlNo, partNo, orderId, partId, startDate, endDate, instane, contractId, warrentyYear, lots, units, price, margin)
            for row in tableData:
                    if not any(row):  # Skip entirely empty rows
                        continue
            for itemName, itemDescription, hsn_sac, productSlNo, partNo, orderId, partId, startDate, endDate, instane, contractId, warrentyYear, lots, units, price, margin in tableData:
                if not any([itemName, itemDescription, hsn_sac, productSlNo, partNo, orderId, partId, startDate, endDate, instane, contractId, warrentyYear, lots, units, price, margin]):
                    continue
                if startDate:
                    possible_dateFormat = ['%d-%m-%Y', '%Y-%m-%d']
                    for date in possible_dateFormat:
                        try:
                            startDate_str = datetime.strptime(startDate, date)
                            print('startDate_str:', startDate_str)    
                        except:
                            pass
                    if startDate_str:
                        startDate_formatted = startDate_str.strftime('%Y-%m-%d')


                    for dateend in possible_dateFormat:
                        try:
                            endDate_str = datetime.strptime(endDate, dateend )    
                        except:
                            pass
                    if endDate_str:
                        endDate_formatted = endDate_str.strftime('%Y-%m-%d')
                else:
                    startDate_formatted=None
                    endDate_formatted=None

                def extractDigit(price):
                    digit = ''.join(filter(str.isdigit, price))
                    return int(digit) if digit else None

                newMargin = int(margin)/100
                newMarginPrice = newMargin*extractDigit(price)
                newUpdatedMarginPrice = newMarginPrice+extractDigit(price)
                unitPriceValue = int(units)*newUpdatedMarginPrice
                unitPriceValueList.append(unitPriceValue)
                totalUnitPriceValue = sum(unitPriceValueList)
                
                print('Unit Price Value', totalUnitPriceValue)
                
                quotationDetails = BOQQuotationTable(itemName=itemName, itemDescription=itemDescription, hsn_sac=hsn_sac, productSlNo=productSlNo, quotationType=quotationType, quotationNo=companyQuotationNoFinal, partNo=partNo, orderId=orderId, partId=partId, startDate=startDate_formatted, endDate=endDate_formatted, instane=instane, contractId=contractId, warrentyYear=warrentyYear, units=units, price=price, margin=margin, totalUnitPrice= newUpdatedMarginPrice, totalAmount= unitPriceValue, currentDate= datetime.now().date(), companyGST=companyGSTRetrieve)
                quotationDetails.save()

                gstApply = int(companyGSTApply)/100 * (totalUnitPriceValue)
                totalAmount = totalUnitPriceValue + gstApply
                totalAmountValue.append(totalAmount)
                print('total amount value', totalAmountValue) 

            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            databaseData = BOQQuotationTable.objects.filter(currentDate = datetime.now().date() , companyGST=companyGSTRetrieve, quotationType=quotationType)
            # print("Database Filtered Data:",databaseData)

            filteredData = []
            for index, row in enumerate(databaseData, start=1):
                rowData = {}
                rowData['SL No.']=index
                if row.itemName:
                    rowData['Item Name'] = row.itemName
                if row.itemDescription:
                    rowData['Item Description'] = row.itemDescription
                if row.hsn_sac:
                    rowData['HSN/SAC'] = row.hsn_sac
                if row.productSlNo:
                    rowData['Product SLNo'] = row.productSlNo
                if row.partNo:
                    rowData['Part No'] = row.partNo
                if row.instane:
                    rowData['Instane'] = row.instane
                if row.contractId:
                    rowData['Contract ID'] = row.contractId
                if row.orderId:
                    rowData['Order ID'] = row.orderId
                if row.partId:
                    rowData['Part ID'] = row.partId
                if row.startDate:
                    rowData['Start Date'] = row.startDate
                if row.endDate:
                    rowData['End Date'] = row.endDate
                if row.warrentyYear:                       
                    rowData['Warrenty Year'] = row.warrentyYear
                if row.units:
                    rowData['Units'] = row.units
                if 'USD' in row.price:
                    rowData['USD_Price'] = row.price
                else:
                    rowData['USD_Price'] = 'NA'
                if row.totalUnitPrice:
                    rowData['Price'] = row.totalUnitPrice
                if row.totalAmount:
                    rowData['Total Amount'] = row.totalAmount
                if rowData:
                    filteredData.append(rowData)

            if filteredData:
                column_names = filteredData[0].keys()
            else:
                column_names = []
            print('Filtered Data:', filteredData)

            data_by_year = defaultdict(list)
            data_by_year_difference =  defaultdict(lambda: {'rows': [], 'subtotal': 0, 'gst': 0, 'total_with_gst': 0})

            for row in filteredData:
                print('inside filtered Data ')
                start_date_str = row.get('Start Date')
                end_date_str = row.get('End Date')

                print('startDate:', start_date_str, 'endDate:', end_date_str)
                if start_date_str and end_date_str:
                    if 'USD' in row['USD_Price']:
                            usd_price = row['USD_Price']
                            
                            yearData = start_date_str.year
                            data_by_year[yearData].append(row)
                        
                    else:        
                        try:  
                            year_diff = end_date_str.year-start_date_str.year
                            total = row['Total Amount']
                            data_by_year_difference[year_diff]['rows'].append(row)
                            data_by_year_difference[year_diff]['subtotal'] += total
                            if year_diff not in data_by_year_difference:
                                data_by_year_difference[year_diff] = []
                            # data_by_year_difference[year_diff].append(row)
                            print('data by difference year:', data_by_year_difference)
                        except ValueError as e:
                            print(e)
                else:
                    pass

            for year_diff, data in data_by_year_difference.items():
                gst_rate = int(companyGSTApply) / 100
                data['gst'] = "{:.2f}".format(Decimal(data['subtotal']) * Decimal(gst_rate))
                data['total_with_gst'] = "{:.2f}".format(Decimal(data['subtotal']) + Decimal(data['gst']))

            if data_by_year and data_by_year_difference:
                
                context = {
                            'companyName':companyName,
                            'companyAddress':companyAddress,
                            'companyGST':companyGST,
                            'companyGSTApply':companyGSTApply,
                            'companyQuotationNo':companyQuotationNoFinal,
                            'quotationType':quotationType,
                            'pricevalidtill':pricevalidtill,
                            'importantNote':importantNote,
                            'deliveryTime':deliveryTime,
                            'companyPayment':companyPayment,
                            'date':formatted_datetime,
                            'price': price,
                            'quotationFor':quotationFor,
                            # 'totalUnitPriceValue':totalUnitPriceValue,
                            'gstApply':gstApply,
                            # 'totalAmount':totalAmount,
                            
                            'data_by_year':dict(data_by_year),
                            'data_by_year_difference': dict(data_by_year_difference),
                            'unique_year_diffs': sorted(data_by_year_difference.keys()),
                            'column_names':column_names,
                            

                }

                print('context', context)

                return render(request, 'generateQuotation.html', context)
            else:
                context = {
                            'companyName':companyName,
                            'companyAddress':companyAddress,
                            'companyGST':companyGST,
                            'companyGSTApply':companyGSTApply,
                            'companyQuotationNo':companyQuotationNoFinal,
                            'quotationType':quotationType,
                            'pricevalidtill':pricevalidtill,
                            'importantNote':importantNote,
                            'deliveryTime':deliveryTime,
                            'companyPayment':companyPayment,
                            'date':formatted_datetime,
                            'price': price,
                            'quotationFor':quotationFor,
                            'totalUnitPriceValue':totalUnitPriceValue,
                            'gstApply':gstApply,
                            'totalAmount':totalAmount,
                            
                            'filteredData':filteredData,
                            'column_names':column_names,
                            

                }

                print('context', context)

                return render(request, 'generateQuotation.html', context)


        elif quotationType == 'BOQ':
            tableData = zip(itemName, itemDescription, hsn_sac, productSlNo, partNo, orderId, partId, startDate, endDate, instane, contractId, warrentyYear, lots, units, price, margin)
            for itemName, itemDescription, hsn_sac, productSlNo, partNo, orderId, partId, startDate, endDate, instane, contractId, warrentyYear, lots, units, price, margin in tableData:
                if not any([itemName, itemDescription, hsn_sac, productSlNo, partNo, orderId, partId, startDate, endDate, instane, contractId, warrentyYear, lots, units, price, margin]):
                    continue
                if startDate:
                    possible_dateFormat = ['%d-%m-%Y', '%Y-%m-%d']
                    for date in possible_dateFormat:
                        try:
                            startDate_str = datetime.strptime(startDate, date)
                            print('startDate_str:', startDate_str)    
                        except:
                            pass
                    if startDate_str:
                        startDate_formatted = startDate_str.strftime('%Y-%m-%d')


                    for dateend in possible_dateFormat:
                        try:
                            endDate_str = datetime.strptime(endDate, dateend )    
                        except:
                            pass
                    if endDate_str:
                        endDate_formatted = endDate_str.strftime('%Y-%m-%d')
                else:
                    startDate_formatted=None
                    endDate_formatted=None
                
                def extractDigit(price):
                    digit = ''.join(filter(str.isdigit, price))
                    return int(digit) if digit else None

                print('margin', margin)
                newMargin = int(margin)/100
                print(newMargin)
                newMarginPrice = newMargin*extractDigit(price)
                newUpdatedMarginPrice = newMarginPrice+extractDigit(price)
                totalAmount = int(units)*newUpdatedMarginPrice
                unitPriceValueList.append(totalAmount)
                totalUnitPriceValue = sum(unitPriceValueList)
                
                gstApply = int(companyGSTApply)/100 * totalUnitPriceValue
                subTotal = gstApply + totalUnitPriceValue


                print('total price', totalUnitPriceValue)
                print('sub total', subTotal)
                
                if lots: 
                    print('inside lots')
                    quotationDetails = BOQQuotationTable(itemName=itemName, itemDescription=itemDescription, hsn_sac=hsn_sac, productSlNo=productSlNo, quotationType=quotationType, quotationNo=companyQuotationNoFinal, partNo=partNo, orderId=orderId, partId=partId, startDate=startDate_formatted, endDate=endDate_formatted, instane=instane, contractId=contractId, warrentyYear=warrentyYear, lots=lots, units=units, price=price, margin=margin, totalUnitPrice= newUpdatedMarginPrice, totalAmount= totalAmount, currentDate= datetime.now().date(), companyGST=companyGSTRetrieve)
                    quotationDetails.save()
                else:
                    print('no lot present')
                    lots = None
                    quotationDetails = BOQQuotationTable(itemName=itemName, itemDescription=itemDescription, hsn_sac=hsn_sac, productSlNo=productSlNo, quotationType=quotationType, quotationNo=companyQuotationNoFinal, partNo=partNo, orderId=orderId, partId=partId, startDate=startDate_formatted, endDate=endDate_formatted, instane=instane, contractId=contractId, warrentyYear=warrentyYear, lots=lots, units=units, price=price, margin=margin, totalUnitPrice= newUpdatedMarginPrice, totalAmount= totalAmount, currentDate= datetime.now().date(), companyGST=companyGSTRetrieve)
                    quotationDetails.save()

            

            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            databaseData = BOQQuotationTable.objects.filter(currentDate = datetime.now().date() , companyGST=companyGSTRetrieve, quotationType=quotationType)
            # print("Database Filtered Data:",databaseData)

            filteredData = []
            for index, row in enumerate(databaseData, start=1):
                rowData = {}
                rowData['SL No.']=index
                if row.itemName:
                    rowData['Item Name'] = row.itemName
                if row.itemDescription:
                    rowData['Item Description'] = row.itemDescription
                if row.hsn_sac:
                    rowData['HSN/SAC'] = row.hsn_sac
                if row.productSlNo:
                    rowData['Product SLNo'] = row.productSlNo
                if row.partNo:
                    rowData['Part No'] = row.partNo
                if row.instane:
                    rowData['Instane'] = row.instane
                if row.contractId:
                    rowData['Contract ID'] = row.contractId
                if row.orderId:
                    rowData['Order ID'] = row.orderId
                if row.partId:
                    rowData['Part ID'] = row.partId
                if row.startDate:
                    rowData['Start Date'] = row.startDate
                if row.endDate:
                    rowData['End Date'] = row.endDate
                if row.warrentyYear:                       
                    rowData['Warrenty Year'] = row.warrentyYear
                if row.units:
                    rowData['Units'] = row.units
                if row.lots:
                    rowData['Lot'] = row.lots
                if row.totalUnitPrice:
                    rowData['Price'] = row.totalUnitPrice
                if row.totalAmount:
                    rowData['Total Amount'] = row.totalAmount
                if rowData:
                    filteredData.append(rowData)

            if filteredData:
                column_names = filteredData[0].keys()
            else:
                column_names = []
            print('Filtered Data:', filteredData)

            
            print('Column Name', column_names)

            if 'Lot' in column_names:
                groupData = defaultdict(lambda: {'rows': [], 'totalPrice': 0, 'rowCount': 0})

                for row in filteredData:
                    lot = row['Lot']
                    print(f"Processing Lot: {lot}, Total Amount (Row): {row['Total Amount']}")

                    groupData[lot]['rows'].append(row)
                    groupData[lot]['totalPrice'] += row['Total Amount']  
                    groupData[lot]['rowCount'] += 1

                # Calculate totals and GST for each lot
                for lot, lotData in groupData.items():
                    totalAmount = lotData['totalPrice']
                    print('totalAmount:', type(totalAmount), totalAmount)

                    print('Total Amount for Lot:', lot, totalAmount)

                    # Calculate GST and total amount including GST
                    gst = Decimal(int(companyGSTApply) / 100) * Decimal(totalAmount)
                    total_with_gst = Decimal(totalAmount) + gst

                    # Update the lot data
                    lotData['totalAmount'] = "{:.2f}".format(Decimal(totalAmount))
                    lotData['gst'] = "{:.2f}".format(gst)
                    lotData['total_with_gst'] = "{:.2f}".format(total_with_gst)
            else:
                groupData = None
               
            if groupData:  
                context = {
                            'companyName':companyName,
                            'companyAddress':companyAddress,
                            'companyGST':companyGST,
                            'companyGSTApply':companyGSTApply,
                            'companyQuotationNo':companyQuotationNoFinal,
                            'quotationType':quotationType,
                            'pricevalidtill':pricevalidtill,
                            'companyPayment':companyPayment,
                            'deliveryTime':deliveryTime, 
                            'importantNote':importantNote,
                            'date':formatted_datetime,
                            'price': price,
                            'quotationFor':quotationFor,
                            'totalAmount':totalAmount,
                            'groupData': dict(groupData),
                            'column_names':column_names,
                            

                }
                print('ContextData is: ', context)
                return render(request, 'generateQuotation.html', context)
            else:
                context = {
                            'companyName':companyName,
                            'companyAddress':companyAddress,
                            'companyGST':companyGST,
                            'companyGSTApply':companyGSTApply,
                            'companyQuotationNo':companyQuotationNoFinal,
                            'quotationType':quotationType,
                            'pricevalidtill':pricevalidtill,
                            'deliveryTime':deliveryTime, 
                            'importantNote':importantNote,
                            'companyPayment':companyPayment,
                            'date':formatted_datetime,
                            'price': price,
                            'quotationFor':quotationFor,
                            'totalAmount':subTotal,
                            'column_names':column_names,
                            'filteredData': filteredData,
                            'totalUnitPriceValue': totalUnitPriceValue,
                            'gstApply': gstApply,


                }
                print('ContextData is: ', context)
                return render(request, 'generateQuotation.html', context)

        else:
            unitPriceValue_list = []
            finalTotalPrice_list = []

            tableData = zip(itemName, itemDescription, hsn_sac, productSlNo, partNo, orderId, partId, startDate, endDate, instane, contractId, warrentyYear, units, price, margin)
            for row in tableData:
                    if not any(row):  # Skip entirely empty rows
                        continue
            for itemName, itemDescription, hsn_sac, productSlNo, partNo, orderId, partId, startDate, endDate, instane, contractId, warrentyYear, units, price, margin in tableData:
                
                if not any([itemName, itemDescription, hsn_sac, productSlNo, partNo, orderId, partId, startDate, endDate, instane, contractId, warrentyYear, lots, units, price, margin]):
                    continue

                
                if startDate:
                    possible_dateFormat = ['%d-%m-%Y', '%Y-%m-%d']
                    for date in possible_dateFormat:
                        try:
                            startDate_str = datetime.strptime(startDate, date)
                            print('startDate_str:', startDate_str)    
                        except:
                            pass
                    if startDate_str:
                        startDate_formatted = startDate_str.strftime('%Y-%m-%d')


                    for dateend in possible_dateFormat:
                        try:
                            endDate_str = datetime.strptime(endDate, dateend )    
                        except:
                            pass
                    if endDate_str:
                        endDate_formatted = endDate_str.strftime('%Y-%m-%d')
                else:
                    startDate_formatted=None
                    endDate_formatted=None

                try:
                    margin = int(margin) if margin.isdigit() else 0
                except (ValueError, TypeError):
                    margin = 0

                try:
                    units = int(units) if units.isdigit() else 0
                except (ValueError, TypeError):
                    units = 0

                try:
                    price = float(price) if price else 0.0
                except (ValueError, TypeError):
                    price = 0.0


                newMargin = int(margin)/100
                newMarginPrice = newMargin*float(price)
                newUpdatedMarginPrice = newMarginPrice+float(price)
                unitPriceValue = int(units)*newUpdatedMarginPrice
                unitPriceValue_list.append(unitPriceValue)

                finalTotalPrice_list.append(newUpdatedMarginPrice)
                
                quotationDetails = BOQQuotationTable(itemName=itemName, itemDescription=itemDescription, hsn_sac=hsn_sac, productSlNo=productSlNo, quotationType=quotationType, quotationNo=companyQuotationNoFinal, partNo=partNo, orderId=orderId, partId=partId, startDate=startDate_formatted, endDate=endDate_formatted, instane=instane, contractId=contractId, warrentyYear=warrentyYear, units=units, price=price, margin=margin, totalUnitPrice= newUpdatedMarginPrice, totalAmount= unitPriceValue, currentDate= datetime.now().date(), companyGST=companyGSTRetrieve)
                quotationDetails.save()

                totalUnitPriceValue = round(sum(unitPriceValue_list), 2)
                finalTotalPrice = sum(finalTotalPrice_list)
                valueToGSTApply = float(companyGSTApply)/100 * float(totalUnitPriceValue)
                gstApply = round((valueToGSTApply), 2)
                totalAmount = round((float(totalUnitPriceValue) + float(gstApply)), 2)
                print('totalUnitPriceValue:', totalUnitPriceValue)
                print('finalTotalPrice:', finalTotalPrice)
                print('GST:', gstApply)
                print('totalAmount:',totalAmount)

            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            databaseData = BOQQuotationTable.objects.filter(currentDate = datetime.now().date() , companyGST=companyGSTRetrieve, quotationType=quotationType)
            print("Database Filtered Data:",databaseData)

            filteredData = []
            for index, row in enumerate(databaseData, start=1):
                rowData = {}
                rowData['SL No.']=index

                if row.itemName:
                    rowData['Item Name'] = row.itemName
                if row.itemDescription:
                    rowData['Item Description'] = row.itemDescription
                if row.hsn_sac:
                    rowData['HSN/SAC'] = row.hsn_sac
                if row.productSlNo:
                    rowData['Product SLNo'] = row.productSlNo
                if row.partNo:
                    rowData['Part No'] = row.partNo
                if row.instane:
                    rowData['Instane'] = row.instane
                if row.contractId:
                    rowData['Contract ID'] = row.contractId
                if row.orderId:
                    rowData['Order ID'] = row.orderId
                if row.partId:
                    rowData['Part ID'] = row.partId
                if row.startDate:
                    rowData['Start Date'] = row.startDate
                if row.endDate:
                    rowData['End Date'] = row.endDate
                if row.warrentyYear:
                    rowData['Warrenty Year'] = row.warrentyYear
                if row.units:
                    rowData['Units'] = row.units
                if row.price:
                    rowData['Price'] = row.totalUnitPrice
                if row.totalAmount:
                    rowData['Total Amount'] = row.totalAmount
                
                
                if rowData:
                    filteredData.append(rowData)

            if filteredData:
                column_names = filteredData[0].keys()
            else:
                column_names = []
            
            print(filteredData)
            context = {
                'companyName':companyName,
                'companyAddress':companyAddress,
                'companyGST':companyGST,
                'companyGSTApply':companyGSTApply,
                'companyQuotationNo':companyQuotationNoFinal,
                'quotationType':quotationType,
                'pricevalidtill':pricevalidtill,
                'deliveryTime':deliveryTime, 
                'importantNote':importantNote,
                'companyPayment':companyPayment,
                'date':formatted_datetime,
                'quotationFor':quotationFor,
                'totalUnitPriceValue':totalUnitPriceValue,
                'gstApply':gstApply,
                'totalAmount':totalAmount,
                'filteredData':filteredData,
                'column_names':column_names,

            }
            
            return render(request, 'generateQuotation.html', context)
        
    return render(request, 'login.html')
        
def getCompanyInfo(request):
    rows = clientDetails.objects.all()
    data = {
        'rows': list(rows.values()),
    }
    return JsonResponse(data)
   
def getClientData(request):
    companyName = request.GET.get('companyname')
    print('Company Name :', companyName)

    company = clientDetails.objects.filter(clientName = companyName)
    for companyData in company:
        clientGST = companyData.GSTDetails,
        clientAddress = companyData.Address,
    
    data = {
            'clientGST':clientGST,
            'clientAddress': clientAddress,
    }
    return JsonResponse(data)


def reviseQuotationData(request): 
    companyName = request.GET.get('companyName')
    print('Data coming from .js',companyName)
    quotationNo = request.GET.get('quotationNo')
    print(quotationNo)

    quotationData = BOQQuotationTable.objects.filter(quotationNo=quotationNo)
    print('Quotation Data:', quotationData)
    
        
    companyGSTFetch = BOQQuotationTable.objects.filter(quotationNo=quotationNo).values('companyGST').first().get('companyGST')
    fetchCompanyName = CompanyDetails.objects.filter(companyGST=companyGSTFetch).values('companyName').first().get('companyName')
    print("Company Name:", fetchCompanyName)
    if fetchCompanyName == companyName:
        filteredData = []
        for index, row in enumerate(quotationData, start=1):
            rowData = {}
            rowData['SL No.']=index

            if row.id:
                rowData['ID'] = row.id
            if row.itemName:
                rowData['Item Name'] = row.itemName
            if row.itemDescription:
                rowData['Item Description'] = row.itemDescription
            if row.hsn_sac:
                rowData['HSN/SAC'] = row.hsn_sac
            if row.productSlNo:
                rowData['Product SLNo'] = row.productSlNo
            if row.partNo:
                rowData['Part No'] = row.partNo
            if row.instane:
                rowData['Instane'] = row.instane
            if row.contractId:
                rowData['Contract ID'] = row.contractId
            if row.orderId:
                rowData['Order ID'] = row.orderId
            if row.partId:
                rowData['Part ID'] = row.partId
            if row.startDate:
                rowData['Start Date'] = row.startDate
            if row.endDate:
                rowData['End Date'] = row.endDate
            if row.warrentyYear:
                rowData['Warrenty Year'] = row.warrentyYear
            if row.units:
                rowData['Units'] = row.units
            if row.price:
                rowData['Price'] = row.newMarginAppliedPrice
            if row.totalAmount:
                rowData['Total Amount'] = row.totalAmount
            if row.margin:
                rowData['Old Margin'] = row.margin
            if row.price:
                rowData['Cost Price'] = row.price
            if rowData:
                filteredData.append(rowData)
            
        context = {
            'filteredData': filteredData,
        }
        print(context)
        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'Enter Valid Quotation ID'}, status=400)
        

@cache_control(no_cache=True, must_revalidate=True)
def generateReviseQuotation(request):
    if request.method == 'POST':
        print('inside generateReviseQuotation')
        try:
            data = json.loads(request.body)
            table_data = data.get('tabledata', [])
            quotationNo = data.get('quotationNo')
            deleted_rows = data.get('deletedRows', [])
            print('Quotation No.:', quotationNo)
            totalUnitPriceList=[]
            marginList=[]
            newPriceList=[]
            print('deleted_rows', deleted_rows)

            if deleted_rows:
                BOQQuotationTable.objects.filter(quotationNo=quotationNo, id__in=deleted_rows).delete()
                cache.clear()
                print(f"Deleted rows with IDs: {deleted_rows}")

            quotationDataNew=BOQQuotationTable.objects.filter(quotationNo=quotationNo)
            print(quotationDataNew)

            def extractDigit(price):
                if not price or not isinstance(price, str):
                    return None
                digit = ''.join(filter(str.isdigit, price))
                try:
                    return int(digit) if digit else None
                except ValueError:
                    print(f"Invalid price format: {price}")
                    return None
            
            for index, (row, data) in enumerate(zip(table_data, quotationDataNew)):
                units = row.get('units')
                costPrice = row.get('costPrice')
                newMargin = row.get('newMargin')
                newPrice = row.get('newPrice')

                print('units:', units)
                print('cost price', costPrice)
                print('NewMargin:', newMargin)
                print('NewPrice:', newPrice)
                print(type(newMargin))
                print(type(newPrice))

                if newMargin == "" and newPrice == "":
                    return render(request, 'error.html', {'error_message':'Plese enter amount to Generate Revise Quotation!!'})
                    
                    
                
                elif newMargin == '0' and newPrice == '0':
                    print('New margin Price', data.newMarginAppliedPrice)
                    data.newMarginPrice = data.newMarginPrice
                    data.newMarginAppliedPrice = data.newMarginAppliedPrice

                    totalUnitPrice = int(units) * float(data.newMarginAppliedPrice)
                    data.newMarginPrice = totalUnitPrice

                    totalUnitPriceList.append(totalUnitPrice)
                    data.save()
                    print('Data when both margin and price is 0', data.newMarginPrice)

                elif newMargin == '0':
                    newPriceList.append(newPrice)
                    print('New Price List', newPriceList)

                    totalUnitPrice = int(units) * float(newPrice)
                    data.newMarginPrice = totalUnitPrice
                    data.newMarginAppliedPrice = newPrice
                    print('New Margin price', data.newMarginPrice)
                    totalUnitPriceList.append(totalUnitPrice)
                    data.save()
                    print('Data when both margin is 0', data.newMarginPrice)


                elif newPrice == '0':

                    marginList.append(newMargin)
                    print('New Margin List', marginList)

                    margin = round(float(newMargin))/ 100
                    marginApply = (margin * extractDigit(costPrice)) + extractDigit(costPrice)
                    totalUnitPrice = int(units) * int(marginApply)

                    data.newMargin = newMargin
                    data.newMarginAppliedPrice = marginApply
                    data.newMarginPrice = totalUnitPrice

                    totalUnitPriceList.append(totalUnitPrice)

                    data.save()
                    print('Data when both price is 0', data.newMarginPrice)
            
            companyGSTFetch = BOQQuotationTable.objects.filter(quotationNo=quotationNo).values('companyGST').first().get('companyGST')
            print('company GST:', companyGSTFetch)
            companyData = CompanyDetails.objects.filter(companyGST=companyGSTFetch)
            print('companyData:', companyData)
            for data in companyData:
                companyName = data.companyName
                companyAddress = data.companyAddress
                paymentTerms = data.paymentTerms
                priceValidTill = data.priceValidTill
                gstApply = data.gstApply
                quotationFor = data.quotationFor
                deliveryTime = data.deliveryTime
                importantNote = data.importantNote

            companyQuotationType = BOQQuotationTable.objects.filter(quotationNo=quotationNo).values('quotationType').first().get('quotationType')  
            print('Company QuotationType:', companyQuotationType)

            totalUnitPriceValue = sum(totalUnitPriceList)
            gstAppliedPrice = int(gstApply)/100
            gstApplied = gstAppliedPrice*totalUnitPriceValue
            subTotal = gstApplied + totalUnitPriceValue

            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            
            filteredData = []
            for index, row in enumerate(quotationDataNew, start=1):
                rowData = {}
                rowData['SL No.']=index

                if row.itemName:
                    rowData['Item Name'] = row.itemName
                if row.itemDescription:
                    rowData['Item Description'] = row.itemDescription
                if row.hsn_sac:
                    rowData['HSN/SAC'] = row.hsn_sac
                if row.productSlNo:
                    rowData['Product SLNo'] = row.productSlNo
                if row.partNo:
                    rowData['Part No'] = row.partNo
                if row.instane:
                    rowData['Instane'] = row.instane
                if row.contractId:
                    rowData['Contract ID'] = row.contractId
                if row.orderId:
                    rowData['Order ID'] = row.orderId
                if row.partId:
                    rowData['Part ID'] = row.partId
                if row.startDate:
                    rowData['Start Date'] = row.startDate
                if row.endDate:
                    rowData['End Date'] = row.endDate
                if row.warrentyYear:
                    rowData['Warrenty Year'] = row.warrentyYear
                if row.units:
                    rowData['Units'] = row.units
                if 'USD' in row.price:
                    rowData['USD_Price'] = row.price
                else:
                    rowData['USD_Price'] = 'NA'
                if row.lots:
                    rowData['Lot'] = row.lots
                if row.newMarginAppliedPrice:
                    rowData['Price'] = row.newMarginAppliedPrice
                if row.newMarginPrice:
                    rowData['Total Amount'] = row.newMarginPrice


                if rowData:
                    filteredData.append(rowData)
            
            print(rowData['Total Amount'])
            print('filtered data:', filteredData)   
            if filteredData:
                column_names = filteredData[0].keys()
            else:
                column_names = []

            

            if companyQuotationType == 'Subscription/Licence':
                data_by_year = defaultdict(list)
                data_by_year_difference =  defaultdict(lambda: {'rows': [], 'subtotal': 0, 'gst': 0, 'total_with_gst': 0})
                for row in filteredData:
                    print('inside filtered Data ')
                    start_date_str = row.get('Start Date')
                    end_date_str = row.get('End Date')
                    print('startDate:', start_date_str, 'endDate:', end_date_str)
                    if start_date_str and end_date_str:
                        
                        if 'USD' in row['USD_Price']:
                                yearData = start_date_str.year
                                data_by_year[yearData].append(row)
                            
                        else:        
                            try:
                                year_diff = end_date_str.year-start_date_str.year
                                print('Year Diff', year_diff)
                                total = row['Total Amount']
                                data_by_year_difference[year_diff]['rows'].append(row)
                                data_by_year_difference[year_diff]['subtotal'] += total
                                if year_diff not in data_by_year_difference:
                                    data_by_year_difference[year_diff] = []
                                # data_by_year_difference[year_diff].append(row)
                                print('data by difference year:', data_by_year_difference)
                            except ValueError as e:
                                print(e)
                    else:
                        print('error')
                for year_diff, data in data_by_year_difference.items():
                    gst_rate = int(gstApply) / 100
                    data['gst'] = float(data['subtotal']) * float(gst_rate)
                    data['total_with_gst'] = float(data['subtotal']) + data['gst']
                if data_by_year and data_by_year_difference:
                    context = {
                                    'companyName':companyName,
                                    'companyAddress':companyAddress,
                                    'companyGST':companyGSTFetch,
                                    'companyQuotationNo':quotationNo,
                                    'quotationType':companyQuotationType,
                                    'pricevalidtill':priceValidTill,
                                    'companyGSTApply':gstApply,
                                    'companyPayment':paymentTerms,
                                    'date':formatted_datetime,
                                    'quotationFor':quotationFor,
                                    'deliveryTime':deliveryTime,
                                    'importantNote':importantNote,

                                    # 'totalUnitPriceValue':totalUnitPriceValue,
                                    'gstApply':gstApply,
                                    # 'totalAmount':totalAmount,
                                    
                                    'data_by_year':dict(data_by_year),
                                    'data_by_year_difference': dict(data_by_year_difference),
                                    'unique_year_diffs': sorted(data_by_year_difference.keys()),
                                    'column_names':column_names,
                                    

                    }
                    print('context:', context)
                    
                    return render(request, 'generateQuotation.html', context)
                else:
                    context = {
                                    'companyName':companyName,
                                    'companyAddress':companyAddress,
                                    'companyGST':companyGSTFetch,
                                    'companyQuotationNo':quotationNo,
                                    'quotationType':companyQuotationType,
                                    'pricevalidtill':priceValidTill,
                                    'companyGSTApply':gstApply,
                                    'companyPayment':paymentTerms,
                                    'date':formatted_datetime,
                                    'quotationFor':quotationFor,
                                    'deliveryTime':deliveryTime,
                                    'importantNote':importantNote,

                                    'totalUnitPriceValue':totalUnitPriceValue,
                                    'gstApply':gstApplied,
                                    'totalAmount':subTotal,
                                    'filteredData':filteredData,
                                    'column_names':column_names,
                                    

                    }
                    print('context:', context)
                    
                    return render(request, 'generateQuotation.html', context)
            
            elif companyQuotationType == 'BOQ':
                if 'Lot' in column_names:
                    groupData = defaultdict(lambda:{'rows': [], 'totalPrice': 0, 'rowCount': 0})

                    for row in filteredData:
                        lot = row['Lot']
                        groupData[lot]['rows'].append(row)
                        groupData[lot]['totalPrice'] += row['Total Amount']
                        groupData[lot]['rowCount'] += 1

                    for lot, lotData in groupData.items():
                        totalAmount = lotData['totalPrice']
                        gst = int(gstApply)/100 * totalAmount
                        total_with_gst = totalAmount + gst
                        
                        lotData['totalAmount'] = totalAmount
                        lotData['gst'] = gst
                        lotData['total_with_gst'] = total_with_gst
                else:
                    groupData = None

                if groupData:
                    context = {
                                'companyName':companyName,
                                'companyAddress':companyAddress,
                                'companyGST':companyGSTFetch,
                                'companyGSTApply':gstApply,
                                'companyQuotationNo':quotationNo,
                                'quotationType':companyQuotationType,
                                'pricevalidtill':priceValidTill,
                                'companyPayment':paymentTerms,
                                'date':formatted_datetime,
                                
                                'quotationFor':quotationFor,
                                'totalAmount':totalAmount,
                                'groupData': dict(groupData),
                                'column_names':column_names,

                    }
                    print('ContextData is: ', context)
                    return render(request, 'generateQuotation.html', context)
                else:
                    context = {
                                'companyName':companyName,
                                'companyAddress':companyAddress,
                                'companyGST':companyGSTFetch,
                                'companyGSTApply':gstApply,
                                'companyQuotationNo':quotationNo,
                                'quotationType':companyQuotationType,
                                'pricevalidtill':priceValidTill,
                                'companyPayment':paymentTerms,
                                'date':formatted_datetime,
                                'totalUnitPriceValue':totalUnitPriceValue,
                                'gstApply':gstApplied,
                                'quotationFor':quotationFor,
                                'totalAmount':subTotal,
                                'column_names':column_names,
                                'filteredData':filteredData,
                                'deliveryTime':deliveryTime,
                                'importantNote':importantNote,

                    }
                    print('ContextData is: ', context)
                    return render(request, 'generateQuotation.html', context)
            else:
                context = {
                                'companyName':companyName,
                                'companyAddress':companyAddress,
                                'companyGST':companyGSTFetch,
                                'companyQuotationNo':quotationNo,
                                'quotationType':companyQuotationType,
                                'pricevalidtill':priceValidTill,
                                'companyGSTApply':gstApply,
                                'companyPayment':paymentTerms,
                                'date':formatted_datetime,
                                'quotationFor':quotationFor,

                                'totalUnitPriceValue':totalUnitPriceValue,
                                'gstApply':gstApplied,
                                'totalAmount':subTotal,
                                'filteredData':filteredData,
                                'column_names':column_names,
                                'deliveryTime':deliveryTime,
                                'importantNote':importantNote,
                                

                }
                
                return render(request, 'generateQuotation.html', context)

        except json.JSONDecodeError:
            return render(request, 'error.html', {'error_message':'invalid Json data'})
        
    else:
        return render(request, 'login.html')

def addNewClient(request):
    if request.method == 'POST':
        companyName = request.POST.get('companyname')
        companyAddress = request.POST.get('address')
        companyGST = request.POST.get('companygst')
        concernPerson = request.POST.get('concernPerson')
        personDesignation = request.POST.get('personDesignation')
        personContactNo = request.POST.get('personContactNo')
        personEmail = request.POST.get('personEmail')

        print('All details', companyName, companyAddress, companyGST, concernPerson, personDesignation, personContactNo, personEmail)

        clientData = clientDetails(clientName=companyName, Address=companyAddress, GSTDetails=companyGST, concernPersonName=concernPerson, Designation= personDesignation, emailID=personEmail, phoneNo=personContactNo)
        clientData.save()

        
        return redirect('/')

@cache_control(no_cache=True, must_revalidate=True)    
def deleteQuotation(request):
    if request.method=='POST':
        quotationNo = request.POST.get('quotationNo')

        quotations = BOQQuotationTable.objects.filter(quotationNo=quotationNo)
        if quotations.exists():
            # Handle the returned queryset (multiple records)
            for quotation in quotations:
                # Process each quotation
                print(quotation.itemName)
                quotation.delete()
                cache.clear()
            
            return render(request, 'error.html', {'error_message':'Quotation Deleted'})
        else:
            return render(request, 'error.html', {'error_message':'No such Quotation exist'})

def getLastQuotation(request):
    lastQuotation = BOQQuotationTable.objects.order_by('id').last()
    if lastQuotation:
        return JsonResponse({'lastQuotation': lastQuotation.quotationNo})
    else:
        return JsonResponse({'lastQuotation': None})