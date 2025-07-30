from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import InvoiceForm, InvoiceItemFormSet

@login_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            formset.instance = invoice
            formset.save()
            return redirect('invoice_detail', invoice.id)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()

    return render(request, 'invoices/invoice_form.html', {
        'form': form,
        'formset': formset
    })

@login_required
def invoice_detail(request, pk):
    from .models import Invoice
    invoice = Invoice.objects.get(pk=pk)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})



from django.shortcuts import get_object_or_404
from .forms import InvoiceItemForm

@login_required
def invoice_add_item(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == 'POST':
        form = InvoiceItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.invoice = invoice
            item.save()
            return redirect('invoice_detail', pk=invoice_id)
    else:
        form = InvoiceItemForm()

    return render(request, 'invoices/invoice_add_item.html', {
        'form': form,
        'invoice': invoice
    })



from django.utils import timezone
from datetime import timedelta
from .models import Invoice

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_at')
    filter_value = request.GET.get('filter')

    if filter_value == '7days':
        date_from = timezone.now() - timedelta(days=7)
        invoices = invoices.filter(created_at__gte=date_from)
    elif filter_value == '1month':
        date_from = timezone.now() - timedelta(days=30)
        invoices = invoices.filter(created_at__gte=date_from)
    elif filter_value == '6months':
        date_from = timezone.now() - timedelta(days=180)
        invoices = invoices.filter(created_at__gte=date_from)

    return render(request, 'invoices/invoice_list.html', {
        'invoices': invoices,
        'filter_value': filter_value
    })


from .utils import render_to_pdf

@login_required
def invoice_pdf(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    pdf = render_to_pdf('invoices/invoice_pdf_template.html', {'invoice': invoice})
    return HttpResponse(pdf, content_type='application/pdf')


from openpyxl import Workbook
from io import BytesIO
from django.http import HttpResponse
from .models import Invoice

@login_required
def export_invoices_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoices"

    # Headers
    ws.append(['Invoice ID', 'Customer', 'Date', 'Total Amount'])

    for inv in Invoice.objects.all().order_by('-created_at'):
        ws.append([
            inv.id,
            inv.customer.name,
            inv.created_at.strftime("%Y-%m-%d"),
            inv.total_amount()
        ])

    # Save to BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="invoices.xlsx"'
    return response

