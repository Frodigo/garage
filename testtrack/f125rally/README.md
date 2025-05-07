# F125Rally - MySQL database for university

The goal of this project is to design a database for a fake University

## Project description

A higher education institution in Poland needs an IT system capable of meeting the following requirements. Design a database to
help realize this system.

1. The database stores information about the institution – address details, contact information for the secretariat, information
about the rector, dean, etc.
2. The institution employs academic staff and collects their data such as first name, last name, gender, phone number, address,
PESEL (national identification number), date of employment, date of termination of employment, bank account number for payment,
etc.
3. Each lecturer can teach several subjects.
4. Student data is stored, enabling their identification within the system (first name, last name, gender, PESEL, date of birth).
5. All students are grouped into groups, which have their year (cohort) name and a supervisor (one of the lecturers).
6. The institution enables tracking of academic progress, offering a record (transcript/index) in which information is stored
about partial grades received by students in particular groups and for particular subjects.
    In addition to partial grades, the database can display the final grade for a given semester.

**Task:**

1. Prepare DDL (Data Definition Language) for structures that reflect a slice of the world described in the description.
    a. Do not prepare test data – focus on designing tables and relationships between them.
    b. The above description is to approximate the domain in which you will be designing the system. During consultations, you may
clarify or change the requirements with the trainer's consent.
2. Generate an ERD (Entity-Relationship Diagram). Arrange the tables in a readable manner.
    a. Save the diagram and place it in the solution directory as a *.png file.
3. If you use graphic editors, be prepared for them to generate additional code that you don't necessarily need – take this into
account and plan to review and clean up the code.

**In essence, the task is to design a database schema for a university system, including data about the institution, staff,
students, groups, subjects, and grades.**

## Use cases

[Use cases](./use-cases.md)

## Diagrams

1. [First, unnormalized diagram](./unnormalized-diagram.md)
2. [Second, normalized diagram](./normalized-diagram-v1.md)
