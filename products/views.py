from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review


def product_list(request):
    products = Product.objects.all()
    return render(request, "dashboard.html", {"products": products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=product)

    # Calculate average rating
    if reviews.exists():
        avg_rating = round(
            sum(review.rating for review in reviews) / reviews.count(), 1
        )
    else:
        avg_rating = 0

    # Add review
    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

        return redirect(f"/products/{product.id}/")

    return render(request, "product.html", {
        "product": product,
        "reviews": reviews,
        "avg_rating": avg_rating,
    })


def compare_prices(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "compare.html", {"product": product})


def price_history(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "history.html", {"product": product})


def recommendations(request, id):
    product = get_object_or_404(Product, id=id)

    all_products = Product.objects.exclude(id=product.id)

    recommended_list = []

    for item in all_products:
        score = 0
        reason = []

        if item.category == product.category:
            score += 40
            reason.append("Same category")

        price_difference = abs(item.price - product.price)

        if price_difference <= 10000:
            score += 30
            reason.append("Similar price range")
        elif price_difference <= 25000:
            score += 15
            reason.append("Nearby budget")

        if item.brand != product.brand:
            score += 10
            reason.append("Alternative brand")

        recommended_list.append({
            "product": item,
            "score": score,
            "reason": ", ".join(reason)
        })

    recommended_list = sorted(
        recommended_list,
        key=lambda x: x["score"],
        reverse=True
    )[:4]

    return render(request, "recommendations.html", {
        "product": product,
        "recommended_list": recommended_list
    })