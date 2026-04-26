Week 3 — Models, Migrations & ORM

In Week 3, I moved from static data and manual lists into real database-driven Django development.

I learned how Django models work, how migrations update database structure, how the admin panel can manage data efficiently, and how ORM connects database content to real web pages.

The weekly project focused on building a complete mini website powered by database models, admin management, dynamic pages, and search/filter logic.

Key Skills Developed

Database & Models

* Created Django models with meaningful fields
* Used field types such as:
    * CharField
    * TextField
    * IntegerField
    * BooleanField
    * DateTimeField
* Used __str__() for readable admin display

Migrations

* Created and applied migrations
* Understood schema changes through:
    * makemigrations
    * migrate
* Added new fields safely
* Removed fields carefully
* Learned data-loss risks during destructive migrations
* Practiced safe migration strategy for preserving data

Django Admin

* Registered models in admin
* Customized admin with:
    * list_display
    * search_fields
    * list_filter
    * ordering
    * readonly_fields
    * list_editable
    * fieldsets
    * list_per_page
* Added computed admin columns

ORM Basics

* Used:
Model.objects.all()
Model.objects.filter()
Model.objects.get()
get_object_or_404()

* Ordered querysets
* Counted results
* Limited results using slicing
* Used case-insensitive searching with icontains

Views & Templates

* Built list pages from database data
* Built detail pages for single objects
* Connected ORM results to templates
* Used loops and empty states
* Used template filters such as:
    * truncatewords
    * linebreaks

Real Features

* Search using GET parameters
* Published / available item filtering
* Latest items section on homepage
* Reusable template includes
* Safer 404 behavior

Week 3 Project

Built a mini database-driven Django website from scratch using all Week 3 concepts.

Project included:

* Two models
* Admin panel management
* Home page with dynamic content
* List page
* Detail page
* Search feature
* Published-only logic
* Ordered latest content
* Reusable templates

Outcome

By the end of Week 3, I understood how Django handles real data and how backend applications are structured around models, migrations, admin tools, ORM queries, and dynamic templates.