from django.contrib.auth.models import User
from products.models import Product
from wishlist.models import Wishlist
from alerts.models import PriceAlert
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, "index.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        User.objects.create_user(username=username, email=email, password=password)
        return redirect("/login/")

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/dashboard/")

    return render(request, "login.html")

@login_required(login_url="/login/")
def dashboard(request):

    query = request.GET.get("q")
    category = request.GET.get("category")

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category and category != "All":
        products = products.filter(category=category)

    context = {
        "products": products,
        "query": query,
        "category": category,
        "total_products": Product.objects.count(),
        "total_users": User.objects.count(),
        "total_wishlist": Wishlist.objects.count(),
        "total_alerts": PriceAlert.objects.count(),
    }

    return render(request, "dashboard.html", context)
    context = {
        "products": products,
        "query": query,
        "total_products": Product.objects.count(),
        "total_users": User.objects.count(),
        "total_wishlist": Wishlist.objects.count(),
        "total_alerts": PriceAlert.objects.count(),
    }

    return render(request, "dashboard.html", context)
def logout_view(request):
    logout(request)
    return redirect("/")
@login_required(login_url="/login/")
def dashboard(request):
    query = request.GET.get("q")

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, "dashboard.html", {"products": products, "query": query})
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def profile(request):
    return render(request, "profile.html")