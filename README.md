01"
## Week 1 — Django Foundations

In Week 1, I focused on learning the fundamentals of Django and how a web application is structured.

I built a multi-page project called City Explorer, which includes dynamic routing, reusable templates, and structured data rendering.

Key skills developed:
- URL routing and named URLs
- Function-based views
- Template inheritance and includes
- Dynamic content rendering with loops and conditions
- Static files integration (CSS)

This week established the foundation for backend development using Django and prepared for handling requests, forms, and databases in later stages.


Week 2 — HTTP & Forms Basics

In Week 2, I focused on understanding how data flows between the user and the server using HTTP methods.

I built a mini Task App that allows adding, listing, updating, deleting, and filtering tasks using form handling and request processing.

Key skills developed:

* Understanding HTTP request/response cycle
* Difference between GET and POST methods
* Handling form data using request.GET and request.POST
* CSRF protection in Django forms
* Redirect pattern (POST → Redirect → GET)
* Using reverse() for clean URL handling
* Managing simple data storage (in-memory / JSON)
* Implementing basic CRUD-like operations without a database
* Filtering data using GET parameters

This week introduced real backend interaction, focusing on how user input is processed and how dynamic applications behave in practice.

Week 3 — Models, Migrations & ORM

In Week 3, I transitioned from temporary data storage into real database-driven development using Django models and ORM.

I built a mini database-powered website with dynamic content management, searchable pages, detail views, and admin-controlled data.

Key skills developed:

* Creating models with meaningful fields
* Understanding field types (CharField, TextField, IntegerField, BooleanField, DateTimeField)
* Running migrations with makemigrations and migrate
* Understanding safe schema changes and migration workflow
* Using Django admin for content management
* Customizing admin with search, filters, ordering, editable fields, and computed columns
* ORM queries using:
    * .all()
    * .filter()
    * .get()
    * get_object_or_404()
* Ordering, counting, slicing, and searching querysets
* Building database-powered list and detail pages
* Search using GET parameters
* Published-only visibility logic
* Reusable templates with {% include %}

This week marked the shift from learning Django syntax to building real backend applications powered by structured data and database logic.
Week 4 — Full CRUD Applications

In Week 4, I expanded my Django projects from read-only database pages into fully interactive CRUD applications.

I built complete frontend management systems where users can create, read, update, and delete database content directly from the website without relying on Django admin.

This week focused heavily on application structure, reusable templates, clean URL design, safe data handling, and real-world backend patterns.

Key skills developed:

* Full CRUD workflow:
    * Create
    * Read
    * Update
    * Delete
* Building frontend forms with POST requests
* Updating existing database objects using .save()
* Safe deletion using POST-only confirmation flows
* Understanding why destructive actions should not use GET requests
* Redirecting after create, edit, and delete actions
* Reusing form templates for both create and edit pages
* Dynamic template behavior using {% if %}
* Organizing templates into feature-based folders
* Creating reusable CSS button systems and shared UI structure
* Working with slug-based URLs using SlugField
* Automatic slug generation using slugify
* Creating reusable slug helper functions
* Understanding route order priority with dynamic slug URLs
* Using relationships with ForeignKey
* Creating related objects through forms and POST data
* Accessing related objects in templates and ORM queries
* Understanding reverse relationships using _set
* Implementing soft delete systems using is_deleted
* Filtering hidden/deleted objects from querysets
* Customizing admin behavior for soft deleted objects
* Improving UX with validation, preserved form input, and dynamic navigation
* Structuring reusable queryset logic appropriately without over-engineering

This week marked the transition from simple database-driven pages into real-world Django application architecture and interactive backend development.