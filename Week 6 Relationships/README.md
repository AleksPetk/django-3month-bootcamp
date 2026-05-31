Week 6 — Relationships & Connected Data

In Week 6, I focused on understanding how Django models connect together and how to build relationship-driven applications using ForeignKey, reverse relations, related_name, and query optimization.

Unlike previous weeks where models were mostly used individually or for filtering, this week focused on how real backend systems are built from connected data.

The week heavily emphasized forward relationships, reverse relationships, relationship chains, model connection design, database integrity rules, and relationship query optimization.

The final project combined multiple connected models into a small blog-style system with teachers, subjects, articles, and comments.

Key Skills Developed

ForeignKey Relationships

Built one-to-many relationships using ForeignKey.

Created connected model structures such as:

Teacher → Articles
Subject → Articles
Article → Comments

Practiced forward relationship access:

article.teacher.name

article.subject.name

comment.article.title

Learned that a ForeignKey stores the related object connection through an ID field, such as:

article.teacher_id

and that:

article.teacher.id

may require loading the related object unless it was already selected.

Reverse Relationships

Practiced reverse relationship access from the parent side.

Examples:

teacher.articles.all()

subject.articles.all()

article.comments.all()

Learned that reverse relations are not normal lists, but related managers that can use QuerySet methods such as:

* .all()
* .filter()
* .count()
* .order_by()
* .exists()
* .first()

Used reverse relations to build pages showing:

* all articles by a teacher
* all articles in a subject
* all comments connected to an article

related_name

Used related_name to replace default reverse relation names.

Changed default names such as:

teacher.article_set.all()

into cleaner names such as:

teacher.articles.all()

Used related_name for:

* teacher.articles
* subject.articles
* article.comments

Learned that related_name affects both reverse access and reverse query traversal.

Examples:

Teacher.objects.filter(articles__published=True)

Subject.objects.filter(articles__difficulty=“Beginner”)

Article.objects.filter(comments__approved=True)

Relationship Naming & Architecture

Learned that related_name is not only for shorter typing, but for clearer relationship meaning.

Discussed when default _set names can be useful for learning and when custom related names become better for real projects.

Practiced relationship naming patterns such as:

* articles
* comments
* followers
* following

Understood that good relationship naming improves readability and maintainability in larger projects.

Multiple ForeignKeys to the Same Model

Built a Follow-style relationship model where the same model appears more than once.

Example:

follower = ForeignKey(Author, related_name=“following”)
following = ForeignKey(Author, related_name=“followers”)

Learned why related_name becomes necessary when one model has multiple ForeignKeys to the same target model.

This made it possible to write:

author.followers.all()

author.following.all()

Bridge / Connection Models

Learned that not every model represents content.

Some models mainly represent relationships or connections, such as:

* follows
* likes
* memberships
* subscriptions
* connections between users

Built a Follow model that mainly stores a connection between two Author objects.

Understood that bridge models can later gain their own metadata, such as:

* created_at
* status
* approved
* notification settings

Database Constraints

Used database-level constraints to protect relationship rules.

Used UniqueConstraint to prevent duplicate connections.

Example:

models.UniqueConstraint(
fields=[“follower”, “following”],
name=“unique_follow_connection”
)

This prevents the same follower/following pair from being saved twice.

Used CheckConstraint to prevent invalid relationships such as self-following.

Example:

models.CheckConstraint(
condition=~models.Q(follower=models.F(“following”)),
name=“prevent_self_follow”
)

Learned that constraints protect data integrity at the database level, not only in the frontend or admin.

Q and F Expressions

Met Q() and F() expressions inside relationship constraints.

Q() was used to build database conditions.

F() was used to compare one model field against another model field.

Example:

models.Q(follower=models.F(“following”))

means:

follower equals following

Using:

~

means NOT.

So:

~models.Q(follower=models.F(“following”))

means:

follower is not equal to following

Also learned logical operators:

* & for AND
* | for OR
* ~ for NOT

Meta Class

Learned that class Meta is used for model metadata and configuration.

Examples of Meta usage:

* ordering
* constraints
* verbose_name
* db_table

Learned that Meta must be called exactly Meta because Django looks for that class name specifically.

Also learned that changing Python behavior like str usually does not require migrations, while changing model fields, relationships, constraints, or Meta options usually does.

Multi-Level Relationship Chains

Practiced moving through multiple connected models.

Examples:

comment.article.teacher.name

comment.article.subject.name

teacher.articles.first().comments.all()

subject.articles.first().teacher.name

Learned that Django relationships create an object graph, and that code can move forward and backward through that graph.

Practiced chains like:

Comment → Article → Teacher

Comment → Article → Subject

Teacher → Articles → Comments

Subject → Articles → Comments

Relationship Filtering

Filtered through relationship chains using double underscores.

Examples:

Comment.objects.filter(article__teacher__is_active=True)

Comment.objects.filter(article__subject__name=“Django”)

Article.objects.filter(comments__approved=True)

Learned that ORM filters can follow relationships across multiple models and generate SQL joins behind the scenes.

Relationship Aggregation & Annotation

Used relationship-based aggregate and annotation logic.

Examples:

Teacher.objects.annotate(
articles_count=Count(“articles”)
)

Teacher.objects.annotate(
total_views=Sum(“articles__views”)
)

Subject.objects.annotate(
avg_rating=Avg(“articles__rating”)
)

Article.objects.annotate(
comments_count=Count(“comments”)
)

Learned the difference between:

aggregate()

and:

annotate()

aggregate() returns one final summary result.

annotate() adds temporary calculated values to each object.

Used annotations to build ranking and dashboard-style pages.

Relationship-Based Pages

Built relationship-driven pages such as:

* teachers page
* teacher detail page
* articles page
* article detail page
* subjects page
* subject detail page
* ranking page

These pages displayed related data such as:

* teacher information on articles
* subject information on articles
* comments connected to articles
* article counts per teacher
* total views per teacher
* average rating per subject
* approved comments only

Relationship Optimization

Learned how related object access can create extra database queries.

Understood the N+1 query problem.

Used select_related() for ForeignKey and OneToOne relationships.

Examples:

Article.objects.select_related(“teacher”, “subject”)

Used prefetch_related() for reverse and many-object relationships.

Examples:

Teacher.objects.prefetch_related(“articles”)

Article.objects.prefetch_related(“comments”)

Used nested optimization paths:

Teacher.objects.prefetch_related(“articles__subject”)

Subject.objects.prefetch_related(“articles__teacher”)

Learned that select_related is best for single-object relationships, while prefetch_related is best for reverse or many-object relationships.

Prefetch

Used Prefetch for filtered and ordered related data.

Example:

Prefetch(
“articles”,
queryset=Article.objects.filter(published=True).order_by(”-created_at”),
to_attr=“published_articles”
)

Learned that to_attr stores prepared related data as a normal Python list.

Example:

teacher.published_articles

Used Prefetch to keep templates clean and avoid filtering related objects inside HTML.

Optimization Mindset

Learned not to optimize blindly.

Important rule:

Only select_related or prefetch_related relationships that the page actually uses.

Examples:

If a template uses:

article.teacher.name

use:

select_related(“teacher”)

If a template loops:

article.comments.all

use:

prefetch_related(“comments”)

If a page does not display related objects, avoid unnecessary optimization.

Final Project

Built a relationship-driven learning blog system from scratch.

Models included:

* Teacher
* Subject
* Article
* Comment

Relationships included:

Teacher → many Articles
Subject → many Articles
Article → many Comments

The project included:

* connected models
* related_name usage
* forward relationship display
* reverse relationship display
* approved comments only
* select_related
* prefetch_related
* relationship-based pages
* clean connected data structure

Important final template understanding:

article.comments

is a reverse manager.

To loop comments in templates, use:

{% for comment in article.comments.all %}

Outcome

By the end of Week 6, I was able to build Django applications based on connected models instead of isolated data.

I learned how to move through relationships forward and backward, how to name reverse relations clearly, how to build relationship-driven pages, how to protect relationship integrity with constraints, and how to optimize related queries with select_related, prefetch_related, and Prefetch.

This week marked the transition from basic database usage into real backend relationship architecture, where models form connected systems and pages are built around those connections.