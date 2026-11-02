from django.test import TestCase
from .models import Product, ShippingBox, CustomerOrder, OrderItem
from .packing_algorithm import Item, pack_items, recommend_box
from .services import recommend_for_order


class PackingAlgorithmTests(TestCase):
    def setUp(self):
        self.small = {"id": 1, "name": "Small", "dimensions": (10, 10, 10),
                      "max_weight": 5, "cost": 20}
        self.large = {"id": 2, "name": "Large", "dimensions": (20, 20, 20),
                      "max_weight": 20, "cost": 35}

    def test_single_item_fits(self):
        items = [Item("Book", (8, 5, 2), 1)]
        self.assertIsNotNone(pack_items(items, self.small["dimensions"]))

    def test_rotation_allows_fit(self):
        items = [Item("Long item", (12, 5, 5), 1)]
        box = (5, 12, 5)
        self.assertIsNotNone(pack_items(items, box))

    def test_item_too_large_does_not_fit(self):
        items = [Item("Oversize", (11, 5, 5), 1)]
        self.assertIsNone(pack_items(items, self.small["dimensions"]))

    def test_two_items_do_not_overlap(self):
        items = [Item("A", (6, 6, 6), 1), Item("B", (6, 6, 6), 1)]
        self.assertIsNone(pack_items(items, (10, 10, 10)))

    def test_weight_limit_rejects_box(self):
        items = [Item("Heavy", (2, 2, 2), 8)]
        result = recommend_box(items, [self.small, self.large])
        self.assertEqual(result["box"]["name"], "Large")
        self.assertIn("Small", [r["name"] for r in result["rejected"]])

    def test_lowest_cost_valid_box_selected(self):
        items = [Item("Item", (4, 4, 4), 1)]
        result = recommend_box(items, [self.large, self.small])
        self.assertEqual(result["box"]["name"], "Small")

    def test_no_box_available(self):
        items = [Item("Huge", (100, 100, 100), 1)]
        result = recommend_box(items, [self.small, self.large])
        self.assertIsNone(result["box"])

    def test_empty_order(self):
        self.assertIsNone(recommend_box([], [self.small])["box"])


class OrderServiceTests(TestCase):
    def test_django_order_recommendation(self):
        product = Product.objects.create(name="Notebook", length=8, width=5, height=2, weight=0.5)
        ShippingBox.objects.create(name="Mailer", inner_length=10, inner_width=10,
                                   inner_height=5, max_weight=2, cost=12)
        order = CustomerOrder.objects.create(reference="ORD-1001")
        OrderItem.objects.create(order=order, product=product, quantity=1)
        result = recommend_for_order(order)
        self.assertEqual(result["box"]["name"], "Mailer")
