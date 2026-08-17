"""Flask REST API for the product catalog."""
from __future__ import annotations

from flask import Flask, jsonify, request, send_from_directory
from db import get_connection, init_db
import os

app = Flask(__name__, static_folder="static", static_url_path="")


@app.before_request
def setup() -> None:
    init_db()


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@app.get("/api/products")
def list_products():
    """Return products filtered by optional query parameters.

    Query params:
      category   – exact match (string)
      brand      – exact match (string)
      min_price  – minimum price inclusive (float)
      max_price  – maximum price inclusive (float)
      in_stock   – "1" to show in-stock items only
      min_rating – minimum rating inclusive (float)
    """
    category   = request.args.get("category")
    brand      = request.args.get("brand")
    min_price  = request.args.get("min_price",  type=float)
    max_price  = request.args.get("max_price",  type=float)
    in_stock   = request.args.get("in_stock")
    min_rating = request.args.get("min_rating", type=float)

    conditions: list[str] = []
    params:     list      = []

    if category:
        conditions.append("category = ?")
        params.append(category)
    if brand:
        conditions.append("brand = ?")
        params.append(brand)
    if min_price is not None:
        conditions.append("price >= ?")
        params.append(min_price)
    if max_price is not None:
        conditions.append("price <= ?")
        params.append(max_price)
    if in_stock == "1":
        conditions.append("is_in_stock = 1")
    if min_rating is not None:
        conditions.append("rating >= ?")
        params.append(min_rating)

    where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    sql = f"""
        SELECT id, name, category, brand, price, is_in_stock, rating
        FROM products
        {where_clause}
        ORDER BY name
    """

    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()

    return jsonify([dict(row) for row in rows])


@app.get("/api/filters")
def filter_options():
    """Return distinct categories and brands for populating dropdowns."""
    with get_connection() as conn:
        categories = [r[0] for r in conn.execute(
            "SELECT DISTINCT category FROM products ORDER BY category"
        ).fetchall()]
        brands = [r[0] for r in conn.execute(
            "SELECT DISTINCT brand FROM products ORDER BY brand"
        ).fetchall()]

    return jsonify({"categories": categories, "brands": brands})


# ---------------------------------------------------------------------------
# Frontend
# ---------------------------------------------------------------------------

@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
