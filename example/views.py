from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect

from example.forms import ProductForm
from example.models import Product


def add_edit_product(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, id=product_id)
    else:
        product = None

    if request.method == 'POST':
        form = ProductForm(instance=product, data=request.POST, files=request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect(reverse('example-edit-product', args=[product.id]))
    else:
        form = ProductForm(instance=product)

    return render(request, 'example/product.html', dictionary={
        'form': form,
        'product': product,
    })
