## Week 9 — Django Class-Based Views (CBVs)

In Week 9, I focused on transitioning from Function-Based Views (FBVs) to Django’s Class-Based Views (CBVs). Rather than simply converting existing views, I learned how Django’s generic views work internally, when to customize them, and how to build complete CRUD features using reusable class-based architecture.

Throughout the week, I converted existing CRUD operations to CBVs, implemented ownership protection, built reusable templates, and created an entirely new Watchlist feature from scratch using Class-Based Views.

Key skills developed:

* Understanding the purpose of Django Generic Views
* Building CRUD applications using:
    * ListView
    * DetailView
    * CreateView
    * UpdateView
    * DeleteView
* Understanding the responsibilities of each CBV
* Configuring generic views using:
    * model
    * form_class
    * template_name
    * context_object_name
    * paginate_by
    * success_url
    * reverse_lazy()
* Understanding URL parameter handling:
    * pk
    * self.kwargs
    * self.get_object()
* Customizing querysets using:
    * get_queryset()
    * filtering objects by owner
    * restricting object visibility
* Customizing page data using:
    * get_context_data()
* Processing forms using:
    * form_valid()
    * form.instance
    * assigning protected fields such as owner = request.user
* Passing custom arguments to forms using:
    * get_form_kwargs()
    * custom init()
    * kwargs.pop()
* Building dynamic ModelForms:
    * hiding fields during updates
    * filtering ForeignKey dropdowns
    * reusing one form for CreateView and UpdateView
* Understanding self.instance:
    * CreateView vs UpdateView
    * avoiding duplicate validation during updates
* Implementing authentication using:
    * LoginRequiredMixin
* Implementing ownership protection using:
    * get_queryset()
    * object filtering by logged-in user
* Understanding permission strategies:
    * get_queryset()
    * UserPassesTestMixin
    * test_func()
    * dispatch()
    * handle_no_permission()
* Building reusable CRUD templates:
    * page_form.html
    * page_delete.html
* Creating reusable CRUD architecture across multiple models
* Building complete CRUD systems using CBVs:
    * Reviews
    * Movies
    * Watchlist
* Using UniqueConstraint together with improved user experience by filtering already-selected objects from form dropdowns
* Understanding when to customize generic views and when to rely on Django’s default behavior
* Learning common CBV hooks:
    * get_queryset()
    * get_context_data()
    * get_form_kwargs()
    * form_valid()
    * get_success_url()
    * delete()
* Understanding the relationship between:
    * Views
    * Forms
    * Models
    * Templates
* Building complete Django features following a professional workflow:
    * Model
    * Migration
    * Admin
    * Form
    * View
    * URL
    * Template
    * CSS

This week marked the transition from writing procedural Function-Based Views to building reusable, maintainable, and scalable Django applications using Class-Based Views. Rather than focusing only on syntax, I learned how generic views organize application logic, encourage code reuse, simplify CRUD development, and provide a clean architecture suitable for larger Django projects.