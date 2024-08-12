from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Sale
from .utils import get_available_printers, print_receipt
from decimal import Decimal
import json

def pos_view(request):
    products = Product.objects.all()
    return render(request, 'pos/pos.html', {'products': products})

def checkout(request):
    if request.method == 'POST':
        cart = json.loads(request.POST.get('cart'))
        total = Decimal(request.POST.get('total'))
        
        sale = Sale.objects.create(
            total=total,
            items=json.dumps(cart)
        )
        
        return redirect('select_printer', sale_id=sale.id)

def select_printer(request, sale_id):
    printers = get_available_printers()
    return render(request, 'pos/select_printer.html', {'printers': printers, 'sale_id': sale_id})

def print_receipt_view(request):
    if request.method == 'POST':
        printer_id = request.POST.get('printer')
        sale_id = request.POST.get('sale_id')
        
        printers = get_available_printers()
        selected_printer = next((p for p in printers if f"{p['vendor_id']}:{p['product_id']}" == printer_id), None)
        
        if not selected_printer:
            messages.error(request, "Tanlangan printer topilmadi.")
            return redirect('select_printer', sale_id=sale_id)
        
        sale = Sale.objects.get(id=sale_id)
        sale_data = {
            'id': sale.id,
            'date': sale.date,
            'items': sale.get_items(),
            'total': sale.total
        }
        
        success = print_receipt(selected_printer, sale_data)
        
        if success:
            messages.success(request, "Chek muvaffaqiyatli chop etildi.")
        else:
            messages.error(request, "Chek chop etishda xatolik yuz berdi.")
        
        return redirect('pos')
