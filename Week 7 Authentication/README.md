## Week 7 — Authentication

In Week 7, I focused on learning how Django handles users, authentication, protected pages, user roles, and ownership-based permissions.

I built a user-based posting system where users can register, log in, log out, create posts, edit only their own posts, delete only their own posts, and access different pages depending on their role.

This week focused on moving from public CRUD-style applications into real user-based web application behavior.

Key skills developed:

* Understanding Django’s built-in User model
* Running built-in authentication migrations
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
* Using LOGIN_URL
* Using LOGIN_REDIRECT_URL
* Using LOGOUT_REDIRECT_URL
* Understanding next= redirects after login
* Redirecting already-authenticated users away from the login page
* Building a custom registration page
* Creating users correctly with:
    * User.objects.create_user()
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
* Creating protected pages with:
    * @login_required
* Understanding the difference between authentication and authorization
* Understanding that hiding links in templates is not enough security
* Adding backend permission checks in views
* Creating staff-only pages using:
    * user.is_staff
* Creating superuser-only pages using:
    * user.is_superuser
* Querying Django’s built-in User model with:
    * User.objects.all()
    * User.objects.count()
    * User.objects.filter()
* Learning Django Groups for access control
* Comparing Groups with custom access models
* Creating custom access models such as:
    * AnimeAccess
* Understanding custom permission decorators
* Creating custom decorators with:
    * @wraps
    * *args
    * **kwargs
* Understanding why decorators can keep views cleaner
* Moving custom decorators into a separate decorators.py file
* Understanding context processors for global template variables
* Using context processors for access flags such as:
    * can_access_movie
* Creating a post model connected to Django’s User model
* Connecting posts to users with:
    * ForeignKey(User)
* Automatically saving the logged-in user as post owner:
    * author=request.user
* Building public posts pages
* Building “My Posts” pages
* Showing published and unpublished posts only to the owner
* Showing edit/delete links only to post owners
* Checking ownership in templates with:
    * post.author == user
    * post.author_id == user.id
* Checking ownership in views with:
    * post.author_id != request.user.id
* Understanding that UI checks are not enough
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
* Styling authentication pages, posts, forms, navigation, and cards with shared CSS

This week marked the transition from building general database-driven Django pages into building real user-based web applications with login systems, registration, protected pages, roles, access control, and ownership permissions.