by [Vinicius M. Grippa](https://www.oreilly.com/search?q=author:%22Vinicius%20M.%20Grippa%22), [Sergey Kuzmichev](https://www.oreilly.com/search?q=author:%22Sergey%20Kuzmichev%22)

Released September 2021

Publisher(s): O'Reilly Media, Inc.

ISBN: 9781492085874

---

## Notes

### Chapter 2. Modeling and Designing Databases

- designing databases can be compared to designing hauses
	- it's hard to build DB or House without a plan
- **how not to develop a database**
	- starting from something like spreadsheet and build on top of it
- **database design process**
	- 3 stages
		- requirements analysis
			- what we need from db
			- what data we will store
			- how data items relates
		- conceptual design
			- do a model of database for example a diagram in MySQL Workbench
		- logical design
			- convert model to a real database
- **the entity relationship model**
	- databases stores info about
		- entities
		- relationships between them
		- example:
			- student, course -> entities
			- enrollment -> relationship between student and course
	- approach
		- ER model -> Entity Relationships
	- attributes
		- composed
		- simple
		- multivalued -> one customer has several phone numbers
			- considerations
				- are all values equivalent?
				- or represent different things?
					- example: phone can be personal number, work number, etc.
		- primary key -> attribute or attributes that guaranteed to be unique
	- representing relationship
		- one-to-many 1:N
		- many-to-many M:N
		- one-to-one 1:1
	- partial and total participation
		- relations can be
			- optional
			- compulsory
		- example: person can be a consumer only when they bought a product -> total participation
		- example 2: consumer can buy a product -> partial participation
	- entity or attribute?
		- objects -> entities
		- information describes these objects -> attributes
		- if object can have a multiple instances -> entity
		- if object can no exist or be unknown -> attribute
	- entity or relationship?
		- nouns -> entities
		- verbs -> relationships
	- intermediate (associate) entities
		- it simplifies many-to-many relationships
		- one many-to-many relationship is two one-to-many relationships for each side
	- weak and strong entities
		- weak entities cannot exist independently in the database

---
#book #MySQL #databases
