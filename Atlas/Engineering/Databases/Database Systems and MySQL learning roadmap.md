## Level 0: Get comfortable with SQL & Tools

**Goal:** Learn basic SQL syntax and how to use MySQL Workbench.

### Topics

- What is SQL? What is a relational database?
- Introduction to MySQL Workbench interface
- Simple data queries and table creation

### Mini-projects

- Connect to a database in MySQL Workbench
- Run basic SQL comments
- Create a table and insert data

---

## Level 1: Core SQL skills

**Goal:** Master CRUD operations and understand how to query and manipulate data.

### Topics

- `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- Filtering: `WHERE`, `BETWEEN`, `LIKE`, `IN`
- Sorting and aliasing

### Mini-projects

- Create a `car` table with at least 5 fields
- Insert and update sample data
- Write queries with conditions

---

## Level 2: Schema design & data modeling

**Goal:** Learn to design normalized relational schemas and write clean, maintainable SQL.

### Topics

- Table relationships (1:1, 1:N, M:N)
- Primary and foreign keys
- Naming conventions and formatting rules
- Basic normalization (1NF, 2NF, 3NF)

### Mini-projects

- Design a schema for a car dealer
- Apply naming standards (e.g. `pk_`, `uq_`, `ix_`)
- Use `FOREIGN KEY` and `AUTO_INCREMENT`

---

## Level 3: Joins and aggregations

**Goal:** Learn to connect multiple tables and summarize data effectively.

### Topics

- `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`
- `GROUP BY`, `HAVING`, aggregate functions (`COUNT`, `AVG`, etc.)
- Subqueries and alternatives (`WITH`, `JOIN`)

### Mini-projects

- Query cars and their groups
- Do some calculations
- Compare `JOIN` vs `WITH` for the same logic

---

## Level 4: Advanced SQL & safety

**Goal:** Write advanced, safe, and well-optimized queries.

### Topics

- `CASE`, `WINDOW FUNCTIONS` (`ROW_NUMBER`, `RANK`)
- SQL_SAFE_UPDATES and `WHERE` clause protection
- Indexing and query optimization
- Common errors and how to debug them

### Mini-projects

- Write a `DELETE` query with and without `SQL_SAFE_UPDATES`
- Use `ROW_NUMBER()` to assign ranking to students
- Set up indexes and test performance

---

## Level 5: ER Diagrams and DDL for real systems

**Goal:** Design and document a complete SQL database from scratch using DDL.

### Topics

- `CREATE TABLE`, `ALTER`, `DROP`, constraints
- ERD creation tools (MySQL Workbench or dbdiagram.io)
- Exporting and cleaning up SQL scripts

### Mini-projects

- Design and build a system for a fictional high school or small clinic
- Export the `.sql` and `.png` files
- Apply formatting and naming conventions

---

## Level 6: Final project — University Management System

**Goal:** Design and present a complete, real-world database project based on requirements.

### Topics

- Apply all previous knowledge to a real brief
- Justify your choices and structure
- Present and explain your work

### Required Deliverables

- SQL file: `wsb_db_YourGroup.sql`
- Diagram file: `wsb_db_YourGroup.png`
- Optional enhancements (triggers, views, indexing, stored functions)

### Project Elements

- University details (name, contacts, roles)
- Staff (personal data, employment details)
- Students (identifiers, group membership)
- Groups (name, year, supervisor)
- Subjects & grades (partial and final)
- Teacher-subject-student relationships

---

#AI #AIgeneratedContent
