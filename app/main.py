"""Flask REST API for the product catalog."""
from __future__ import annotations

from flask import Flask, jsonify, request, send_from_directory
from db import get_connection, init_db
import os

app = Flask(__name__, static_folder="static", static_url_path="")

# Initialise the database once at startup
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


    sql = """
        SELECT id, name, category, brand, price, is_in_stock, rating
        FROM products
        WHERE
            (:category IS NULL OR category = :category)
            AND (:brand IS NULL OR brand = :brand)
            AND (:min_price IS NULL OR price >= :min_price)
            AND (:max_price IS NULL OR price <= :max_price)
            AND (:in_stock IS NULL OR is_in_stock = :in_stock)
            AND (:min_rating IS NULL OR rating >= :min_rating)
        ORDER BY name
    """

    params = {
        "category": category or None,
        "brand": brand or None,
        "min_price": min_price,
        "max_price": max_price,
        "in_stock": 1 if in_stock == "1" else None,
        "min_rating": min_rating,
    }

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
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, port=port)
