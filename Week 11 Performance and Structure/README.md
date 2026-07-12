## Week 11 — Django Performance & Project Structure

In Week 11, I focused on improving Django application performance and organizing larger projects more professionally.

Throughout the week, I learned how Django loads related objects, how inefficient queries create the N+1 problem, how to reduce unnecessary database work, and how to structure views, services, utilities, validators, and settings so the project remains readable and maintainable as it grows.

Key skills developed:

* Understanding the N+1 query problem
* Using Django Debug Toolbar to inspect:
    * total SQL queries
    * duplicated queries
    * query execution time
    * template-triggered database queries
* Understanding how pagination affects query counts
* Understanding why pagination adds a COUNT query
* Optimizing ForeignKey and OneToOne relationships using:
    * select_related()
* Understanding how select_related() uses SQL JOINs
* Understanding when to use select_related()
* Understanding when not to use select_related()
* Optimizing multiple relationships in one query:
    * author
    * category
* Traversing deeper relationships using:
    * author__profile
* Understanding that select_related() works with:
    * ForeignKey
    * OneToOneField
* Understanding why select_related() does not work well for:
    * reverse ForeignKey relationships
    * ManyToManyField relationships
* Optimizing reverse relationships using:
    * prefetch_related()
* Understanding how prefetch_related() performs:
    * one query for parent objects
    * one query for related objects
    * relationship matching in Python memory
* Using Prefetch objects for advanced related-object loading
* Filtering prefetched objects using custom querysets
* Ordering prefetched comments before attaching them to posts
* Using to_attr to store prefetched results under custom attributes
* Combining:
    * prefetch_related()
    * Prefetch()
    * select_related()
* Preventing nested N+1 queries when comments access their authors
* Building and optimizing a comment system connected to posts and users
* Displaying recent comments on post list pages
* Building a separate page for all comments belonging to a post
* Implementing comment creation, editing, and deletion
* Returning JSON responses for asynchronous frontend actions
* Understanding the difference between:
    * normal Django form submission
    * AJAX/fetch requests
    * full page reloads
    * JSON responses
* Understanding QuerySet lazy evaluation
* Understanding when Django actually sends SQL to the database
* Understanding QuerySet result caching
* Reusing evaluated QuerySets to avoid repeated queries
* Using exists() when only a yes/no answer is needed
* Using count() when only the number of matching rows is needed
* Understanding count() vs len()
* Using first() and last() safely
* Understanding how model Meta ordering affects first() and last()
* Loading selected database columns using:
    * only()
* Excluding large database columns using:
    * defer()
* Understanding deferred field loading and the extra queries it can create
* Testing performance with:
    * thousands of objects
    * more than 100,000 objects
    * paginated and non-paginated pages
* Understanding that database speed is only one part of page performance
* Understanding the performance cost of:
    * creating Django model objects
    * rendering templates
    * generating large HTML responses
    * browser DOM rendering
* Understanding practical page-size limits and why large datasets require:
    * pagination
    * filtering
    * search
* Learning project structure best practices
* Understanding when to keep a single:
    * views.py
    * forms.py
    * models.py
    * admin.py
* Understanding when to split modules into packages
* Splitting views by feature using:
    * views/__init__.py
    * post_views.py
    * comment_views.py
    * account_views.py
    * other_views.py
* Updating urls.py to import views from multiple modules
* Understanding why views.py and a views/ package can conflict
* Following a safe refactoring workflow:
    * move code
    * update imports
    * test
    * remove or rename old code
* Understanding Python relative imports such as:
    * from ..models import Post
    * from ..forms import PostForm
* Organizing URL routes by feature
* Organizing imports into:
    * standard-library imports
    * Django imports
    * third-party imports
    * local application imports
* Understanding circular imports
* Understanding how dependency direction helps prevent circular imports
* Learning the purpose of utils.py
* Creating utility functions for:
    * custom image upload paths
    * UUID-based filenames
    * JSON-ready comment response data
* Understanding that utility functions should usually:
    * perform one small reusable task
    * avoid request handling
    * avoid controlling business workflows
* Learning the purpose of services.py
* Moving image-processing logic from models into a service function
* Creating service functions for:
    * post image processing
    * OpenAI API communication
    * OpenAI response parsing
    * OpenAI error extraction
* Understanding that services contain business logic and multi-step actions
* Understanding the difference between:
    * utils.py
    * services.py
    * models.py
    * views.py
    * forms.py
* Keeping views focused on request and response handling
* Keeping models focused on database behavior
* Keeping forms focused on validation and input handling
* Keeping services focused on application work
* Keeping utilities focused on small reusable helpers
* Avoiding unnecessary recursive model saves
* Updating database fields directly when model save recursion should be avoided
* Closing Pillow image files safely using context managers
* Creating named constants for:
    * maximum image dimensions
    * JPEG quality
    * API timeout
    * maximum output tokens
    * maximum upload size
* Organizing settings.py into clear sections
* Adding useful module, class, and function docstrings
* Adding comments only where logic is not immediately obvious
* Removing or clearly labeling autogenerated and memo code
* Organizing admin.py, forms.py, models.py, services.py, utils.py, validators.py, and urls.py consistently
* Creating and protecting environment variables using:
    * .env
    * .gitignore
* Keeping API keys outside source code
* Connecting a Django website helper to the OpenAI Responses API
* Configuring AI helper behavior using:
    * instructions
    * model settings
    * token limits
    * timeout handling
    * fallback responses
    * API error handling

This week marked the transition from building Django features that simply work to building Django applications that remain fast, organized, readable, and easier to maintain as their data, features, and codebase grow. I learned how query optimization, pagination, project structure, services, utilities, and clear responsibility boundaries work together to create more professional Django applications.