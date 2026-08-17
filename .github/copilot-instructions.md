# Copilot Code Review Instructions for SQL

When reviewing SQL code in this repository, apply the following best practices. Flag any violations and suggest improvements.

## Naming Conventions

- Use **lowercase snake_case** for table names, column names, and aliases (e.g., `customer_order`, `first_name`).
- Use descriptive, meaningful names — avoid abbreviations like `c`, `t1`, or `tmp` unless context is obvious.
- Prefix boolean columns with `is_`, `has_`, or `can_` (e.g., `is_active`, `has_discount`).

## SELECT Clauses

- **Never use `SELECT *`** in production queries. Always specify the exact columns needed.
- Qualify all column references with a table name or alias when joining multiple tables to prevent ambiguity.
- Avoid selecting duplicate columns or columns that are not used by the calling code.

## WHERE Clauses and Filtering

- Always include a `WHERE` clause on `UPDATE` and `DELETE` statements unless a full-table operation is explicitly intended and documented.
- Avoid applying functions to indexed columns on the left-hand side of a condition (e.g., `WHERE YEAR(created_at) = 2024`) as this prevents index use; rewrite as range comparisons (`WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01'`).
- Use `IS NULL` / `IS NOT NULL` instead of `= NULL` / `!= NULL`.
- Prefer explicit `JOIN` conditions over implicit cross joins in the `FROM` clause.
- Avoid catch-all optional-filter predicates such as `(:param IS NULL OR column = :param)` in production queries on large tables, because they often prevent selective index use.
- Prefer handling optional filter logic in application code by building query predicates only for provided filters, while still using parameterized values.

## JOINs

- Always use explicit `JOIN` syntax (`INNER JOIN`, `LEFT JOIN`, etc.) rather than comma-separated tables in `FROM`.
- Specify the join type explicitly; do not rely on the default `JOIN` (even though it is equivalent to `INNER JOIN`) — explicit is better.
- Ensure every `JOIN` has a proper `ON` condition. Flag any Cartesian products unless they are intentional and documented.
- Use `LEFT JOIN` with a `WHERE IS NULL` check instead of `NOT IN` subqueries when checking for non-existence, to handle `NULL` values correctly and improve performance.

## Subqueries and CTEs

- Prefer **Common Table Expressions (CTEs)** over nested subqueries for readability.
- Avoid correlated subqueries in `SELECT` lists or `WHERE` clauses when a `JOIN` can achieve the same result more efficiently.
- Give CTEs descriptive names that reflect what they represent (e.g., `active_customers`, `monthly_revenue`).

## NULL Handling

- Be explicit about `NULL` handling — use `COALESCE` or `NULLIF` where appropriate.
- Avoid comparisons that silently ignore `NULL` values (e.g., `NOT IN` lists containing `NULL` members).
- Document columns that are intentionally nullable.

## Aggregations and GROUP BY

- Every non-aggregated column in the `SELECT` list must appear in the `GROUP BY` clause.
- Do not use column positions in `ORDER BY` or `GROUP BY` (e.g., `GROUP BY 1, 2`); use column names or aliases instead.
- Filter aggregated results using `HAVING`, not `WHERE`.

## Indexes and Performance

- Flag queries that perform a full table scan on large tables without an indexed filter.
- Avoid `SELECT DISTINCT` as a substitute for fixing duplicate-producing joins; instead fix the root cause.
- Be cautious with `OR` conditions on different columns — they can prevent index use; consider rewriting as `UNION ALL`.
- Avoid leading wildcards in `LIKE` patterns (e.g., `LIKE '%value'`) on indexed columns.

## Data Modification (INSERT / UPDATE / DELETE)

- Always wrap multi-statement data modifications in a transaction when atomicity is required.
- Prefer `MERGE` (or equivalent upsert syntax) over separate `INSERT`/`UPDATE` pairs to avoid race conditions.
- Validate that `DELETE` and `UPDATE` statements target only the intended rows; suggest a corresponding `SELECT` to preview affected rows.

## Schema and DDL

- Every table should have a clearly defined **primary key**.
- Foreign key constraints should be defined explicitly to enforce referential integrity.
- Prefer appropriate, specific data types over generic ones (e.g., use `DATE` instead of `VARCHAR` for dates, `BOOLEAN` instead of `TINYINT(1)` where supported).
- Add `NOT NULL` constraints where a column should never be null.
- Include indexes on columns that are frequently used in `WHERE`, `JOIN`, or `ORDER BY` clauses.

## Security

- **Never interpolate user input directly into SQL strings.** Always use parameterized queries or prepared statements to prevent SQL injection.
- Avoid granting excessive privileges (e.g., `GRANT ALL`); use least-privilege access.
- Do not store sensitive data (passwords, PII) in plaintext; flag any such patterns.

## Style and Formatting

- Use consistent indentation (2 or 4 spaces) — do not mix tabs and spaces.
- Capitalize SQL keywords (`SELECT`, `FROM`, `WHERE`, `JOIN`, `ON`, `AND`, `OR`, etc.).
- Place each major clause (`SELECT`, `FROM`, `WHERE`, `GROUP BY`, `ORDER BY`) on its own line.
- Limit line length to 120 characters; break long expressions across multiple lines.
- Add comments to explain non-obvious logic, especially for complex `WHERE` conditions or business rules embedded in queries.

## General

- Ensure queries are idempotent where possible (especially migrations and seed scripts).
- Avoid hard-coded values that should be parameterized or stored in configuration.
- Review that any dynamically generated SQL is still validated against the above rules.
