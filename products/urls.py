from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="products"),
    path("<int:id>/", views.product_detail, name="product_detail"),
    path("<int:id>/compare/", views.compare_prices, name="compare_prices"),
    path("<int:id>/history/", views.price_history, name="price_history"),
    path("<int:id>/recommendations/", views.recommendations, name="recommendations"),
]