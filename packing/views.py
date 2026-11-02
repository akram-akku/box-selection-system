from django.shortcuts import get_object_or_404, render
from .models import CustomerOrder, Product, ShippingBox
from .services import recommend_for_order


def dashboard(request):
    return render(request, "packing/dashboard.html", {
        "orders": CustomerOrder.objects.order_by("-created_at")[:10],
        "product_count": Product.objects.count(),
        "box_count": ShippingBox.objects.count(),
    })


def recommend(request):
    result = None
    order = None
    if request.method == "POST":
        order = get_object_or_404(CustomerOrder, pk=request.POST.get("order_id"))
        result = recommend_for_order(order)
    return render(request, "packing/recommendation.html", {
        "orders": CustomerOrder.objects.order_by("-created_at"),
        "result": result,
        "selected_order": order,
    })
