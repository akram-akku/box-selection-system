# BoxFit — AI-Assisted Box Selection System

A small Django application that recommends the lowest-cost shipping box that passes a weight-capacity check and a heuristic 3D placement check for every physical item in an order.

## Features
- Product catalogue with dimensions and weight.
- Shipping-box catalogue with internal dimensions, maximum weight and cost.
- Orders with multiple products and quantities.
- Rotation-aware 3D placement heuristic.
- Lowest-cost valid box selection with rejection explanations.
- Django admin for maintaining products, boxes and orders.
- Automated tests and GitHub Actions workflow.

## Requirements
- Python 3.10+
- pip

## Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open `http://127.0.0.1:8000/` and use **Manage data** to add products, boxes and orders. Then select an order on **Start recommendation**.

## Example data to enter
Dimensions are in centimetres, weight in kilograms and cost in your chosen currency.

| Product | L | W | H | Weight |
|---|---:|---:|---:|---:|
| Notebook | 8 | 5 | 2 | 0.5 |
| Bottle | 6 | 6 | 18 | 0.7 |

| Box | Inner L | Inner W | Inner H | Max weight | Cost |
|---|---:|---:|---:|---:|---:|
| Small Mailer | 10 | 10 | 5 | 2 | 12 |
| Medium Box | 20 | 15 | 20 | 10 | 22 |

Create order `ORD-1001`, add one Notebook, and run the recommendation.

## Algorithm and assumptions
1. Expand order quantities into individual physical items.
2. Reject a box if total order weight exceeds its maximum capacity.
3. Sort items largest-volume-first to reduce fragmentation.
4. For each item, try all unique axis-aligned rotations.
5. Try deterministic corner/extreme positions generated from previously placed items.
6. Reject a placement if it exceeds a box dimension or overlaps a placed item.
7. Among boxes for which the heuristic finds a placement, select the lowest cost. Ties are resolved by the sum of dimensions and then box name.

**Important limitation:** 3D bin packing is computationally difficult. This implementation is a deterministic heuristic, not a mathematical proof that a box is impossible to pack. A failed placement means this heuristic did not find a valid arrangement; it does not prove that no arrangement exists. It does not model padding, fragile-item rules, stacking strength, void fill, product-specific orientation restrictions or carrier dimensional-weight pricing. Those would be sensible production extensions.

All dimensions must use the same unit. All product weights and box capacities must use the same weight unit. Costs must use the same currency.

## Tests
```bash
python manage.py test
```
Tests cover rotation, oversize items, non-overlap, weight limits, lowest-cost selection, no valid box, empty orders and the Django order service.

## AI assistance disclosure
See [AI_USAGE.md](AI_USAGE.md). The assignment also asks for a chat transcript and a personal learning reflection. Add your own genuine transcript export and write the reflection yourself; do not submit AI-generated versions of either.

## Repository setup
Create a GitHub repository, then:
```bash
git init
git add .
git commit -m "Build Django box selection system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/box-selection-system.git
git push -u origin main
```
Replace the remote URL with your actual repository URL.
