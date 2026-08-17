# sql-best-practices

A repository demonstrating SQL best practices through a working example application.

## Example Application — Product Catalog

A Python + SQLite web app with a filterable product catalog.

### Stack
- **Backend**: Python / Flask REST API
- **Database**: SQLite (Python built-in `sqlite3`)
- **Frontend**: Single-page vanilla HTML/JS app (no build step)

### Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed the database (creates products.db in the repo root)
cd app
python seed.py

# 3. Start the server
python main.py
```

Then open http://localhost:5000 in your browser.

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/products` | List products with optional filters |
| GET | `/api/filters` | Distinct categories and brands for dropdowns |

#### `/api/products` query parameters

| Param | Type | Description |
|-------|------|-------------|
| `category` | string | Exact category match |
| `brand` | string | Exact brand match |
| `min_price` | float | Minimum price (inclusive) |
| `max_price` | float | Maximum price (inclusive) |
| `in_stock` | `1` | Show in-stock items only |
| `min_rating` | float | Minimum rating (inclusive) |

### Project Structure

```
app/
  db.py          # SQLite connection helper & schema init
  seed.py        # Seeds the database with sample products
  main.py        # Flask application
  static/
    index.html   # Frontend SPA
requirements.txt
products.db      # Created at runtime (git-ignored)
```