from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PriceAlert
from products.models import Product

@login_required(login_url="/login/")
def create_alert(request, id):

    product = Product.objects.get(id=id)

    if request.method == "POST":
        target_price = request.POST.get("target_price")

        PriceAlert.objects.create(
            user=request.user,
            product=product,
            target_price=target_price
        )

        return redirect(f"/products/{product.id}/")

    return render(request, "alert.html", {"product": product})