"""Seed the products table with sample data."""
from db import init_db, get_connection

PRODUCTS = [
    ("Wireless Headphones Pro",   "Electronics", "SoundMax",   89.99,  1, 4.5),
    ("Bluetooth Speaker Mini",    "Electronics", "SoundMax",   39.99,  1, 4.2),
    ("USB-C Hub 7-in-1",          "Electronics", "TechGear",   49.99,  1, 4.7),
    ("Mechanical Keyboard RGB",   "Electronics", "TechGear",  119.99,  0, 4.6),
    ("4K Webcam",                 "Electronics", "VisionTech",  79.99, 1, 4.3),
    ("Noise-Cancelling Earbuds",  "Electronics", "SoundMax",   59.99,  1, 4.4),
    ("Smart LED Desk Lamp",       "Home",        "LumiHome",   34.99,  1, 4.1),
    ("Air Purifier Compact",      "Home",        "PureAir",   129.99,  1, 4.8),
    ("Coffee Maker Drip 12-Cup",  "Home",        "BrewMaster",  49.99, 0, 4.0),
    ("Robot Vacuum Gen2",         "Home",        "CleanBot",  249.99,  1, 4.6),
    ("Non-Stick Pan Set",         "Home",        "CookPro",    39.99,  1, 3.9),
    ("Yoga Mat Premium",          "Sports",      "FlexFit",    29.99,  1, 4.5),
    ("Adjustable Dumbbells 20kg", "Sports",      "IronCore",  149.99,  1, 4.7),
    ("Resistance Bands Set",      "Sports",      "FlexFit",    19.99,  1, 4.3),
    ("Foam Roller Deep Tissue",   "Sports",      "IronCore",   24.99,  0, 4.2),
    ("Running Shoes Trail X",     "Sports",      "SwiftStep",  89.99,  1, 4.6),
    ("Python Programming Book",   "Books",       "TechPress",  34.99,  1, 4.9),
    ("Clean Code: A Handbook",    "Books",       "TechPress",  39.99,  1, 4.8),
    ("Data Science Fundamentals", "Books",       "LearnHub",   29.99,  0, 4.4),
    ("SQL in 10 Minutes",         "Books",       "LearnHub",   24.99,  1, 4.5),
    ("Desk Organiser Bamboo",     "Office",      "OfficePro",  22.99,  1, 4.0),
    ("Ergonomic Mouse Pad",       "Office",      "TechGear",   15.99,  1, 4.1),
    ("Standing Desk Converter",   "Office",      "OfficePro", 199.99,  1, 4.7),
    ("Monitor Light Bar",         "Office",      "LumiHome",   44.99,  1, 4.5),
    ("Cable Management Kit",      "Office",      "TechGear",    9.99,  0, 3.8),
]


def seed() -> None:
    init_db()
    with get_connection() as conn:
        with conn:  # single transaction — rolls back if executemany fails
            conn.execute("DELETE FROM products")
            conn.executemany(
                """
                INSERT INTO products (name, category, brand, price, is_in_stock, rating)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                PRODUCTS,
            )
    print(f"Seeded {len(PRODUCTS)} products.")


if __name__ == "__main__":
    seed()
