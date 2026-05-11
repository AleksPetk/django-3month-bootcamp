Week 4 — Full CRUD Applications

In Week 4, I focused on building complete frontend-controlled CRUD applications using Django.

Unlike previous weeks where most database management happened through Django admin, this week introduced fully interactive website functionality where users can create, edit, update, and delete content directly from the frontend.

The week focused heavily on application structure, reusable templates, URL architecture, safe request handling, relationships between models, and real-world backend patterns.

The final project combined all previous Django concepts into a complete database-driven application with clean structure and reusable logic.

Key Skills Developed

Full CRUD Workflow

Built complete CRUD systems for database objects:

* Create new objects from frontend forms
* Read/display database content
* Update existing objects
* Delete objects safely using POST requests

Frontend Form Handling

* Built frontend forms using HTML + Django views
* Handled form data using request.POST
* Processed checkboxes, text fields, textareas, and date inputs
* Preserved form input during validation errors
* Added validation and user feedback messages
* Redirected users after successful actions

Detail & Dynamic Pages

* Built dynamic detail pages using:
    * <int:id>
    * <slug:slug>
* Improved navigation between:
    * list pages
    * detail pages
    * edit pages
    * delete pages

URL Structure & Routing

* Designed clean URL structures such as:
/posts/
posts/create/
posts/django-basics/
posts/django-basics/edit/
posts/django-basics/delete/
* Learned importance of URL order priority with dynamic slug routes
* Used named URLs consistently throughout templates and views

Reusable Templates

* Reused one form template for both:
    * create pages
    * edit pages
* Used dynamic template rendering with {% if %}
* Organized templates into feature-based folders:
templates/
    posts/
    books/
Slugs & SEO-Friendly URLs

* Used SlugField
* Generated automatic slugs using slugify
* Built reusable slug helper functions
* Understood slug uniqueness and URL-safe naming
* Switched detail pages from ID-based URLs to slug-based URLs

Relationships Between Models

* Built model relationships using ForeignKey
* Connected models such as:
    * Company → Car
    * Author → Book
* Created related objects through forms and POST data
* Accessed related data in templates:
book.author.name
* Used reverse relations:
author.book_set.all()
Delete & Soft Delete Systems

* Built POST-only delete confirmation pages
* Learned why delete actions should not use GET requests
* Implemented soft delete using:
is_deleted = models.BooleanField(default=False)
* Hid deleted objects from public querysets
* Customized admin filtering for soft deleted objects

Django Admin Improvements

* Customized admin panels using:
    * list_display
    * list_filter
    * search_fields
    * ordering
* Created custom admin column labels
* Filtered visible/deleted objects inside admin

CSS & UI Structure

* Built reusable button systems
* Shared CSS classes across pages
* Improved form layouts, detail pages, and delete confirmation pages
* Focused on clean and reusable frontend structure instead of isolated page styling

Final Project

Built a complete CRUD application from scratch including:

* Multiple related models
* Slug-based detail pages
* Full create/edit/delete flows
* Soft delete system
* Search functionality
* Reusable templates
* Organized project structure
* Dynamic frontend interaction

Outcome

By the end of Week 4, I was able to build fully interactive database-driven Django applications with real CRUD functionality, clean architecture, reusable frontend/backend patterns, model relationships, slug routing, and safer data management techniques.

This week marked the transition from basic Django development into building structured, scalable web applications with real backend logic and frontend interaction.