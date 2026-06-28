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


## Week 2 — HTTP & Forms Basics

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

## Week 3 — Models, Migrations & ORM

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

## Week 4 — Full CRUD Applications

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

## Week 5 — Advanced ORM

In Week 5, I focused on understanding Django ORM more deeply and building advanced search, filtering, sorting, and query behavior.

I built a searchable and filterable content system where users can dynamically control which database records are shown using GET parameters, multiple filters, ordering options, and relationship-based search.

This week focused less on CRUD mechanics and more on backend data logic, QuerySet behavior, and building scalable filtering systems.

Key skills developed:

* Advanced filtering using:
    * `.filter()`
    * `.exclude()`
    * `__gt`
    * `__gte`
    * `__lt`
    * `__lte`
    * `__in`
    * `__range`
    * `__isnull`
* Building search systems with:
    * `icontains`
    * GET parameters
    * preserved search values
    * `Q()` objects
    * OR conditions
* Filtering through relationships using ForeignKey fields, such as:
    * `studio__name`
    * `studio__country`
* Dynamic sorting with `.order_by()`
* Sorting from GET parameters, such as:
    * newest
    * oldest
    * highest rating
    * lowest rating
    * related model name
* Understanding QuerySet behavior:
    * lazy evaluation
    * chaining
    * caching basics
    * when database queries actually execute
* Comparing:
    * `.count()` vs `len()`
    * `.get()` vs `.filter()`
    * `.exists()`
    * `.first()`
    * `.last()`
* Using QuerySet slicing for limited results
* Using lightweight query outputs:
    * `.values()`
    * `.values_list()`
    * `flat=True`
    * `.distinct()`
* Using aggregate calculations:
    * `Avg`
    * `Max`
    * `Min`
    * `Sum`
* Using annotations with `annotate()` and `Count`
* Understanding `select_related()` for ForeignKey optimization
* Building progressive filtering logic step-by-step
* Creating advanced filtering pages with:
    * search
    * studio filter
    * genre multi-select
    * rating filter
    * year filter
    * multiplayer filter
    * deleted visibility toggle
    * sorting dropdown
* Using `getlist()` for multi-select filters
* Using `__in` for multiple selected values
* Adding reset filter links for GET-based filtering systems
* Building dashboard-style statistics from filtered QuerySets
* Improving filter UX with basic and advanced filter sections using `<details>`

This week marked the transition from simply accessing database records to controlling, analyzing, filtering, and optimizing data like a real backend application.

## Week 6 — Relationships

In Week 6, I focused on understanding how Django models connect together and how to build relationship-driven applications.

I built a connected blog-style system where teachers, subjects, articles, and comments are linked through ForeignKey relationships and reverse relations.

This week focused less on individual models and more on how data moves between connected models in real backend systems.

Key skills developed:

* Creating one-to-many relationships with ForeignKey
* Understanding forward relationship access, such as:
    * article.teacher.name
    * article.subject.name
    * comment.article.title
* Understanding reverse relationships using related_name, such as:
    * teacher.articles.all()
    * subject.articles.all()
    * article.comments.all()
* Replacing default _set reverse access with cleaner related_name
* Filtering through relationship chains using double underscores, such as:
    * articles__published=True
    * comments__approved=True
    * article__teacher__is_active=True
* Building multi-level relationship chains across connected models
* Using annotate() with relationship counts and totals
* Using Count, Sum, and Avg across related models
* Understanding bridge/connection models such as follow relationships
* Using UniqueConstraint to prevent duplicate relationships
* Using CheckConstraint, Q(), and F() to protect relationship rules
* Understanding class Meta for model-level configuration
* Understanding the N+1 query problem
* Optimizing ForeignKey relationships with select_related()
* Optimizing reverse relationships with prefetch_related()
* Using Prefetch() for filtered or ordered related data
* Building relationship-based pages such as:
    * teacher detail pages
    * subject detail pages
    * article detail pages
    * comments connected to articles
    * ranking/dashboard pages

This week marked the transition from working with separate database tables to building connected backend systems where models interact through clear relationships and optimized queries.

## Week 7 — Authentication

In Week 7, I focused on learning how Django handles users, authentication, protected pages, roles, access control, and ownership-based permissions.

I built a user-based posting system where users can register, log in, log out, create posts, edit only their own posts, delete only their own posts, and access different pages depending on their role.

This week focused on moving from public database-driven applications into real user-based web application behavior.

Key skills developed:

* Understanding Django’s built-in User model
* Running Django’s built-in authentication migrations
* Creating a superuser
* Understanding request.user
* Understanding AnonymousUser
* Checking authentication status with:
    * request.user.is_authenticated
    * user.is_authenticated
* Accessing user fields such as:
    * user.username
    * user.email
    * user.id
    * user.is_staff
    * user.is_superuser
    * user.is_active
    * user.date_joined
    * user.last_login
* Building custom login views using:
    * authenticate()
    * login()
    * logout()
* Understanding that authenticate() returns a User object or None
* Understanding that login() creates the session
* Understanding that logout() removes the session
* Using Django’s built-in LoginView
* Using Django’s built-in LogoutView
* Understanding that built-in LogoutView requires POST
* Configuring authentication redirects with:
    * LOGIN_URL
    * LOGIN_REDIRECT_URL
    * LOGOUT_REDIRECT_URL
* Understanding next= redirects after login
* Redirecting already-authenticated users away from the login page
* Building a custom registration page
* Creating users correctly with User.objects.create_user()
* Understanding why User.objects.create() should not be used for passwords
* Adding registration validation:
    * duplicate username check
    * duplicate email check
    * password length check
    * password confirmation
    * .strip() cleanup for username and email
* Preserving valid form fields after registration errors
* Never preserving password fields
* Auto-logging users in after registration
* Adding simple JavaScript for show/hide password behavior
* Building role-based pages for:
    * normal users
    * staff users
    * superusers
* Creating protected pages with @login_required
* Understanding the difference between authentication and authorization
* Understanding that hiding links in templates is not enough security
* Adding backend permission checks in views
* Creating staff-only pages using user.is_staff
* Creating superuser-only pages using user.is_superuser
* Querying Django’s built-in User model with:
    * User.objects.all()
    * User.objects.count()
    * User.objects.filter()
* Learning Django Groups for access control
* Comparing Groups with custom access models
* Creating custom access models such as AnimeAccess
* Understanding custom permission decorators
* Creating custom decorators with:
    * @wraps
    * *args
    * **kwargs
* Moving custom decorators into a separate decorators.py file
* Understanding context processors for global template variables
* Using context processors for access flags such as can_access_movie
* Creating a Post model connected to Django’s User model
* Connecting posts to users with ForeignKey(User)
* Automatically saving the logged-in user as post owner with author=request.user
* Building public post pages
* Building “My Posts” pages
* Showing published and unpublished posts only to the owner
* Showing edit/delete links only to post owners
* Checking ownership in templates with:
    * post.author == user
    * post.author_id == user.id
* Checking ownership in views with:
    * post.author_id != request.user.id
* Blocking direct URL access for non-owners
* Creating edit pages that only owners can access
* Creating delete pages that only owners can access
* Using POST for dangerous actions like delete and logout
* Understanding the pattern:
    * GET = show confirmation page
    * POST = perform delete
* Using author_id=request.user.id for efficient ownership filtering
* Using class Meta ordering for posts
* Creating reusable templates for post create/edit forms
* Styling authentication pages, post pages, forms, navigation, and cards with shared CSS

This week marked the transition from building general database-driven Django pages into building real user-based web applications with login systems, registration, protected pages, roles, access control, and ownership permissions.

## Week 8 — Django Forms

In Week 8, I focused on learning Django Forms and ModelForms to handle user input in a cleaner, safer, and more maintainable way.

I refactored projects that previously relied on manual request.POST.get() handling into form-driven applications using forms.py, validation methods, reusable templates, and ModelForms connected directly to database models.

This week focused heavily on form validation, reusable CRUD architecture, user registration forms, and separating responsibilities between forms, views, and models.

Key skills developed:

* Understanding the role of forms.py in Django applications
* Understanding the difference between:
    * forms.Form
    * forms.ModelForm
* Building forms using:
    * forms.CharField
    * forms.EmailField
    * forms.IntegerField
    * forms.BooleanField
    * forms.PasswordInput
    * forms.Textarea
    * forms.TextInput
    * forms.Select
    * forms.NumberInput
    * forms.CheckboxInput
* Understanding widgets and how they control HTML display
* Adding widget attributes such as:
    * class
    * placeholder
    * rows
    * min
    * max
    * type=“date”
* Connecting forms directly to models using ModelForm
* Understanding ModelForm Meta configuration:
    * model
    * fields
    * labels
    * help_texts
    * widgets
* Understanding why fields is usually safer than exclude
* Understanding why fields = “all” can be risky in user-facing forms
* Processing form submissions with:
    * request.POST
    * form.is_valid()
    * form.cleaned_data
* Understanding the difference between:
    * raw POST data
    * validated cleaned_data
* Understanding the validation lifecycle:
    * built-in field validation
    * clean_()
    * clean()
    * forms.ValidationError
    * self.add_error()
* Implementing field-level validation with clean_(), including:
    * minimum length checks
    * maximum length checks
    * bad word filtering
    * password length validation
    * rating validation
    * description length validation
* Implementing form-level validation with clean(), including:
    * password confirmation
    * username/password similarity checks
    * start date and end date comparison
    * title/content relationship checks
    * name/description relationship checks
    * recommendation rules based on rating
* Understanding when to use:
    * clean_() for single-field validation
    * clean() for multi-field validation
    * self.add_error() to attach multi-field errors to a specific field
* Transforming cleaned data using:
    * strip()
    * title()
    * lower()
* Saving ModelForms using:
    * form.save()
    * form.save(commit=False)
* Understanding commit=False as a way to create a model object without saving immediately
* Assigning protected fields in views, such as:
    * author = request.user
    * owner = request.user
* Understanding that request belongs to views, not forms, unless explicitly passed
* Editing existing objects using:
    * instance=object
* Understanding the difference between:
    * no instance = create new object
    * instance=object = edit existing object
* Overriding save() inside forms
* Building a custom user registration ModelForm
* Adding password confirmation as a form-only field
* Hashing user passwords correctly with:
    * set_password()
* Auto-logging users in after registration
* Understanding why passwords should not be saved directly with plain form.save()
* Using ForeignKey fields inside ModelForms
* Understanding that ForeignKey fields automatically become dropdown select fields
* Understanding why str() matters for dropdown display
* Building reusable templates:
    * form_page.html
    * delete_form.html
* Passing reusable context variables such as:
    * form
    * page_title
    * button_text
    * cancel_url
    * object
    * page_title_name
* Reusing one form template across create and edit pages
* Reusing one delete confirmation template across different models
* Building complete ModelForm CRUD systems, including:
    * Task CRUD
    * Event CRUD
    * Category CRUD
    * Review CRUD
* Building a Mini Review Board project with:
    * public reviews
    * categories
    * review creation
    * review editing
    * review deletion
    * user registration
    * owner-based permissions
* Using @login_required to protect form pages
* Checking ownership in views before edit/delete actions
* Using request.user.is_superuser for restricted category management
* Using POST-only confirmation for delete actions
* Using select_related() to optimize ForeignKey queries in review lists
* Styling form-driven pages with reusable CSS and shared templates

This week marked the transition from manually handling user input with request.POST.get() to building professional Django applications using forms, validation, reusable templates, and ModelForms that keep validation logic, user input rules, view flow, and database saving properly separated.

## Week 9 — Class-Based Views

In Week 9, I focused on learning Django Class-Based Views and how common CRUD patterns can be built using Django’s generic views.

I converted Function-Based Views into Class-Based Views, built user-owned CRUD features, and practiced using built-in CBV hooks to control querysets, forms, permissions, redirects, and template context.

This week focused heavily on understanding how Django organizes repeated view logic through generic views, while also learning when Function-Based Views may still be clearer for custom logic.

Key skills developed:

* Understanding the difference between Function-Based Views and Class-Based Views
* Using Django generic views:
    * ListView
    * DetailView
    * CreateView
    * UpdateView
    * DeleteView
* Understanding how .as_view() connects CBVs to urls.py
* Understanding Django’s pk convention for object URLs
* Using ListView to display multiple objects
* Customizing ListView with:
    * model
    * template_name
    * context_object_name
    * paginate_by
    * get_queryset()
    * get_context_data()
* Adding pagination with:
    * page_obj
    * paginator
    * is_paginated
* Using DetailView to display one object
* Understanding how DetailView replaces get_object_or_404()
* Using CreateView to create database objects
* Using UpdateView to edit existing database objects
* Using DeleteView to delete objects through confirmation pages
* Understanding which CBVs need form_class and which do not
* Using reverse_lazy() for CBV redirects
* Using form_valid() to add protected fields before saving, such as:
    * owner = request.user
    * user = request.user
* Understanding the CBV version of form.save(commit=False)
* Using get_success_url() for dynamic redirects after saving
* Using get_queryset() for ownership-based access control
* Comparing permission patterns:
    * get_queryset()
    * dispatch()
    * UserPassesTestMixin
    * test_func()
    * handle_no_permission()
* Using LoginRequiredMixin instead of @login_required for CBVs
* Passing custom data from views to forms using get_form_kwargs()
* Using custom form init() methods with kwargs.pop()
* Filtering ForeignKey dropdowns based on the logged-in user
* Reusing one ModelForm for both create and update behavior
* Understanding self.instance in ModelForms during create vs update
* Preventing duplicate records using:
    * UniqueConstraint
    * filtered form querysets
* Building reusable form and delete templates with CBVs
* Building complete CBV-based features, including:
    * Movie CRUD
    * Watchlist CRUD
    * Game Backlog project
* Understanding when CBVs reduce repeated CRUD code
* Understanding when FBVs may be clearer for custom logic
* Thinking about views by feature rather than putting everything into one large file
* Understanding when to split views.py into feature-based files such as:
    * content_views.py
    * review_views.py
    * account_views.py

This week marked the transition from writing manual view logic with Function-Based Views to using Django’s generic Class-Based Views for reusable CRUD architecture, ownership-based access control, cleaner form handling, and more structured backend development.