from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('create_user', views.createNewUser, name='create_user'),
    path('generate_quotation', views.generate_quotation, name='generate_quotation'),
    path('api/getCompanyInfo/', views.getCompanyInfo, name='getCompanyInfo'),
    path('api/getClientData/', views.getClientData, name='getClientData'),
    path('reviseQuotationData/', views.reviseQuotationData, name='reviseQuotationData'),
    path('generateReviseQuotation/', views.generateReviseQuotation, name='generateReviseQuotation'),
    path('generateReviseQuotationFormat/', views.generateReviseQuotation, name='generateReviseQuotationFormat'),
    path('addNewClient', views.addNewClient, name='addNewClient'),
    path('deleteQuotation', views.deleteQuotation, name='deleteQuotation'),
    path('getLastQuotation/', views.getLastQuotation, name='getLastQuitation'),
    path('fetchVendors/', views.fetchVendors, name='fetchVendors'),
    path('askPrice', views.askPrice, name='askPrice'),
]
