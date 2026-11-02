# AI Usage Disclosure

This file documents the assistance used while preparing this starter project. Review it and correct anything that does not accurately describe your own actions before submitting.

## 1. AI tools used
- ChatGPT (OpenAI), for project planning, code drafting, test-case suggestions and documentation structure.

## 2. Prompts used
The main prompt supplied in this conversation was the assignment brief titled **“Python/Django Hiring Assignment: AI-Assisted Box Selection System”**. It described an ecommerce warehouse use case and requested a Django system that recommends a shipping box using product dimensions/weight and box dimensions/weight capacity/cost.

Follow-up request: **“Based on above description prepare a project and give me.”**

## 3. Output accepted
- A Django project structure using SQLite and Django ORM.
- Product, shipping-box, order and order-item models.
- A separate recommendation service and packing algorithm.
- Rotation-aware placement checks and weight-capacity filtering.
- Lowest-cost selection among boxes accepted by the heuristic.
- Django admin screens, a simple Bootstrap interface, tests and GitHub Actions configuration.

## 4. Output rejected or modified
- No claim of an AI-trained or machine-learning model: the recommendation is deterministic rule-based optimization/heuristics, not machine learning.
- The packing method is described as a heuristic rather than a guarantee of optimal 3D packing.
- The chat transcript and “What did you learn?” reflection are deliberately not generated here because the assignment says those must be completed by the candidate without AI.

## 5. Mistakes or limitations to check
- A heuristic may fail to find a valid arrangement even when a different arrangement exists.
- The current model does not include padding, fragile-item constraints, stacking strength, carrier dimensional weight or product orientation restrictions.
- The project uses a development-only Django secret key and `DEBUG=True`; production deployment requires secure settings.
- You should inspect the algorithm, run the tests yourself and be ready to explain every design decision.

## 6. Verification
The project includes automated tests in `packing/tests.py` and a GitHub Actions workflow in `.github/workflows/tests.yml`. Run `python manage.py test` locally and record the real output in `TEST_OUTPUT.md`. Do not claim tests passed until you have run them successfully.

## Candidate review
Before submitting, add a short note here describing what you personally inspected, changed and verified. Do not copy a statement you cannot support with your own work.
