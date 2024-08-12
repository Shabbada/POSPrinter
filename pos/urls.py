from django.urls import path
from . import views

urlpatterns = [
    path('', views.pos_view, name='pos'),
    path('checkout/', views.checkout, name='checkout'),
    path('select-printer/<int:sale_id>/', views.select_printer, name='select_printer'),
    path('print-receipt/', views.print_receipt_view, name='print_receipt'),
]
