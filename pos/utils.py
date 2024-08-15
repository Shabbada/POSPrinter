import usb.core
import usb.util
from escpos.printer import Usb

def get_available_printers():
    printers = []
    devices = usb.core.find(find_all=True)
    
    for dev in devices:
        print(dev.bDeviceClass)
        try:
            if dev:#.bDeviceClass == 7:  # Printer class
                printer = {
                    'name': usb.util.get_string(dev, dev.iProduct),
                    'vendor_id': dev.idVendor,
                    'product_id': dev.idProduct
                }
                printers.append(printer)
        except:
            continue
    
    return printers

def print_receipt(printer_info, sale_data):
    try:
        p = Usb(printer_info['vendor_id'], printer_info['product_id'])
        
        p.set(align='center', font='a', width=2, height=2)
        p.text("Mening Do'konim\n\n")
        
        p.set(align='left', font='a', width=1, height=1)
        p.text(f"Chek №: {sale_data['id']}\n")
        p.text(f"Sana: {sale_data['date'].strftime('%Y-%m-%d %H:%M')}\n\n")
        
        p.text("Mahsulotlar:\n")
        p.text("-" * 32 + "\n")
        for item in sale_data['items']:
            p.text(f"{item['name'][:20]:<20}")
            p.text(f"{item['price']:>10.2f}\n")
        p.text("-" * 32 + "\n")
        
        p.set(align='right', font='a', width=1, height=2)
        p.text(f"Jami: {sale_data['total']:.2f}\n\n")
        
        p.set(align='center', font='a', width=1, height=1)
        p.text("Xaridingiz uchun rahmat!\n")
        p.text("Yana kelib turing\n\n")
        
        p.cut()
        return True
    except Exception as e:
        print(f"Chop etishda xatolik: {e}")
        return False
