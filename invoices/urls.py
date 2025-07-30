from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.invoice_create, name='invoice_create'),
    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('', views.invoice_list, name='invoice_list'),
    path('pdf/<int:pk>/', views.invoice_pdf, name='invoice_pdf'),
    path('export/excel/', views.export_invoices_excel, name='export_invoices_excel'),
    path('<int:invoice_id>/add-item/', views.invoice_add_item, name='invoice_add_item'),
]
