from .models import ShippingBox
from .packing_algorithm import Item, recommend_box


def recommend_for_order(order):
    items = []
    for line in order.items.select_related("product").all():
        p = line.product
        for index in range(line.quantity):
            items.append(Item(
                name=f"{p.name} #{index + 1}",
                dimensions=(float(p.length), float(p.width), float(p.height)),
                weight=float(p.weight),
            ))

    boxes = [{
        "id": box.id,
        "name": box.name,
        "dimensions": (float(box.inner_length), float(box.inner_width), float(box.inner_height)),
        "max_weight": float(box.max_weight),
        "cost": float(box.cost),
    } for box in ShippingBox.objects.all()]

    return recommend_box(items, boxes)
