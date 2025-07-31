from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from invoices.models import Invoice, InvoiceItem
from customers.models import Customer
from products.models import Product
from django.db.models import Sum, Q
from django.utils.timezone import now
from datetime import timedelta
import calendar

@login_required
def dashboard_view(request):
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    total_invoices = Invoice.objects.count()
    total_revenue = sum(inv.total_amount() for inv in Invoice.objects.all())

    # Monthly revenue for last 6 months
    monthly_sales = []
    month_labels = []
    for i in range(5, -1, -1):
        month = now().replace(day=1) - timedelta(days=i*30)
        month_start = month.replace(day=1)
        next_month = (month.replace(day=28) + timedelta(days=4)).replace(day=1)
        month_name = calendar.month_name[month.month]
        month_labels.append(month_name)

        month_invoices = Invoice.objects.filter(created_at__gte=month_start, created_at__lt=next_month)
        month_total = sum(inv.total_amount() for inv in month_invoices)
        monthly_sales.append(round(month_total, 2))

    # Top 5 selling products by quantity
    top_products = (
        InvoiceItem.objects
        .values('product__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:5]
    )
    product_labels = [p['product__name'] for p in top_products]
    product_qty = [p['total_qty'] for p in top_products]

    # 🔍 Search logic
    query = request.GET.get('q')
    customer_result = None
    customer_invoices = None
    product_result = None
    product_invoice_items = None

    if query:
        # Search customer by name, contact, gstin
        customer_result = Customer.objects.filter(
            Q(name__icontains=query) |
            Q(contact__icontains=query) |
            Q(gstin__icontains=query)
        ).first()

        if customer_result:
            customer_invoices = Invoice.objects.filter(customer=customer_result)

        # Search product by name
        product_result = Product.objects.filter(
            name__icontains=query
        ).first()

        if product_result:
            product_invoice_items = InvoiceItem.objects.filter(product=product_result)

    return render(request, 'dashboard/dashboard.html', {
        'total_customers': total_customers,
        'total_products': total_products,
        'total_invoices': total_invoices,
        'total_revenue': total_revenue,
        'month_labels': month_labels,
        'monthly_sales': monthly_sales,
        'product_labels': product_labels,
        'product_qty': product_qty,
        'query': query,
        'customer_result': customer_result,
        'customer_invoices': customer_invoices,
        'product_result': product_result,
        'product_invoice_items': product_invoice_items,
    })
