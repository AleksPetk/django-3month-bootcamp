## Week 8 — Django Forms

In Week 8, I focused on learning Django Forms and ModelForms to handle user input in a cleaner, safer, and more maintainable way.

I refactored projects that previously relied on request.POST.get() into form-driven applications using forms.py, validation methods, reusable templates, and ModelForms connected directly to database models.

This week focused heavily on form validation, reusable CRUD architecture, user registration forms, and separating responsibilities between forms, views, and models.

Key skills developed:

* Understanding the role of forms.Form and forms.ModelForm
* Building forms using:
    * forms.CharField
    * forms.IntegerField
    * forms.BooleanField
    * forms.PasswordInput
    * forms.Textarea
    * forms.Select
    * forms.NumberInput
    * forms.CheckboxInput
* Connecting forms to models using ModelForm
* Understanding Meta configuration:
    * model
    * fields
    * labels
    * help_texts
    * widgets
* Processing forms with:
    * request.POST
    * form.is_valid()
    * form.cleaned_data
* Understanding the validation lifecycle:
    * clean_<field>()
    * clean()
    * forms.ValidationError
    * self.add_error()
* Implementing field-level validation:
    * minimum length checks
    * maximum length checks
    * bad word filtering
    * password requirements
    * rating validation
* Implementing multi-field validation:
    * password confirmation
    * username/password similarity checks
    * start and end date validation
    * title/content relationship checks
    * recommendation rules based on ratings
* Transforming cleaned data:
    * strip()
    * formatting returned values
* Saving ModelForms using:
    * form.save()
    * form.save(commit=False)
* Assigning protected fields such as:
    * author = request.user
    * owner = request.user
* Editing objects using:
    * instance=object
* Overriding save() inside forms
* Building user registration forms with:
    * password confirmation
    * hashed passwords using set_password()
    * automatic login after registration
* Understanding the difference between:
    * browser validation (required)
    * Django form validation (required=True)
* Using ForeignKey fields inside ModelForms:
    * automatic <select> generation
    * dropdown choices from related models
    * importance of __str__()
* Building reusable templates:
    * form_page.html
    * delete_form.html
* Passing reusable context variables:
    * form
    * page_title
    * button_text
    * cancel_url
    * object
    * page_title_name
* Building complete CRUD systems with ModelForms:
    * Category CRUD
    * Review CRUD
    * Event CRUD
* Implementing permission checks:
    * @login_required
    * ownership verification
    * request.user.is_superuser
* Using select_related() to optimize related object queries
* Creating cleaner, reusable, and scalable form-driven applications

This week marked the transition from manually handling user input with request.POST.get() to building professional Django applications using forms, validation, reusable templates, and ModelForms that keep validation logic, business rules, and database interactions properly separated. 