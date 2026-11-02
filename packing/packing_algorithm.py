"""
A deterministic 3D placement heuristic.

This is a practical heuristic, not a proof of optimal 3D bin packing.
It tests all axis-aligned rotations and a set of corner/extreme points.
Dimensions use one consistent unit (for example, centimetres); weights and
costs must also use consistent units/currency.
"""
from dataclasses import dataclass
from itertools import permutations


@dataclass(frozen=True)
class Item:
    name: str
    dimensions: tuple[float, float, float]
    weight: float


@dataclass(frozen=True)
class Placement:
    item_name: str
    origin: tuple[float, float, float]
    dimensions: tuple[float, float, float]


def rotations(dimensions):
    # Remove duplicate rotations when two or more sides are equal.
    return sorted(set(permutations(tuple(float(v) for v in dimensions), 3)),
                  key=lambda d: (d[2], d[1], d[0]))


def overlaps(a_origin, a_size, b_origin, b_size):
    return all(
        a_origin[i] < b_origin[i] + b_size[i] and
        b_origin[i] < a_origin[i] + a_size[i]
        for i in range(3)
    )


def pack_items(items, box_dimensions):
    """Return placements if every item can be placed, otherwise None."""
    box = tuple(float(v) for v in box_dimensions)
    if any(v <= 0 for v in box):
        return None

    # Largest-volume items first reduces common fragmentation failures.
    ordered = sorted(items, key=lambda item: (
        -item.dimensions[0] * item.dimensions[1] * item.dimensions[2],
        -max(item.dimensions),
        item.name,
    ))
    placements = []

    for item in ordered:
        placed = False
        points = {(0.0, 0.0, 0.0)}
        for p in placements:
            x, y, z = p.origin
            dx, dy, dz = p.dimensions
            points.update({(x + dx, y, z), (x, y + dy, z), (x, y, z + dz)})

        # Prefer low, then back, then left positions for reproducibility.
        for origin in sorted(points, key=lambda p: (p[2], p[1], p[0])):
            for size in rotations(item.dimensions):
                if any(origin[i] + size[i] > box[i] + 1e-9 for i in range(3)):
                    continue
                if any(overlaps(origin, size, old.origin, old.dimensions)
                       for old in placements):
                    continue
                placements.append(Placement(item.name, origin, size))
                placed = True
                break
            if placed:
                break
        if not placed:
            return None
    return placements


def recommend_box(items, boxes):
    """
    items: iterable of Item instances (one per physical product unit)
    boxes: iterable of dicts with id, name, dimensions, max_weight, cost
    Returns a result dict with selected box, placement plan and rejection notes.
    """
    items = list(items)
    if not items:
        return {"box": None, "placements": [], "reason": "The order has no items.",
                "rejected": []}

    total_weight = sum(float(item.weight) for item in items)
    rejected = []
    candidates = []

    for box in boxes:
        if total_weight > float(box["max_weight"]) + 1e-9:
            rejected.append({"name": box["name"], "reason": "Maximum weight capacity exceeded."})
            continue
        plan = pack_items(items, box["dimensions"])
        if plan is None:
            rejected.append({"name": box["name"], "reason": "Items could not be placed without exceeding dimensions or overlapping."})
            continue
        candidates.append((float(box["cost"]), sum(box["dimensions"]), box["name"], box, plan))

    if not candidates:
        return {"box": None, "placements": [], "reason": "No available box can safely fit this order.",
                "rejected": rejected}

    # Lowest cost first; then smaller box volume and name for stable tie-breaking.
    candidates.sort(key=lambda c: (c[0], c[1], c[2]))
    _, _, _, selected, plan = candidates[0]
    return {"box": selected, "placements": plan,
            "reason": "Selected the lowest-cost box that passed weight and 3D placement checks.",
            "rejected": rejected}
