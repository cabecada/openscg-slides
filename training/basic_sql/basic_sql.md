---
title: Basic SQL
---

# SQL Primer

[$<]

* Data Definition Language (DDL)
    - CREATE TABLE 
    - DROP TABLE
    - CREATE SEQUENCE
    - DROP SEQUENCE
* Data Manipulation Language (DML)
    - SELECT
    - INSERT
    - UPDATE
    - DELETE

[>$]

***
# CREATE TABLE (simple form)

[$<]

Syntax

```
CREATE TABLE table_name (
    col_1	data_type,
    col_2	data_type, …
    col_n	data_type
);
```

Example

```
CREATE TABLE departments(
    department_id	integer,
    name		varchar(50)
);
```

[>$]

