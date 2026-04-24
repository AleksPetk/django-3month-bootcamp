Week 2 — HTTP & Forms Basics

📚 Overview

This week focuses on understanding how data is exchanged between the user and the server using HTTP methods.

Main goal:

* Learn how to handle user input
* Understand how Django processes requests
* Build interactive features using forms

⸻

🧠 Topics Covered

* HTTP request/response cycle
* GET vs POST methods
* Reading data with request.GET
* Handling form submissions with request.POST
* CSRF protection ({% csrf_token %})
* Redirect pattern (POST → Redirect → GET)
* URL reversing using reverse()
* Passing data through query parameters
* Basic state management (in-memory / JSON)

⸻

🛠 Project Built

Mini Task App

A simple interactive task manager that includes:

* Adding tasks via form (POST)
* Displaying task list
* Deleting tasks
* Marking tasks as done / pending
* Filtering tasks using GET parameters
* Showing total task count

⸻

⚙️ Features Implemented

* Form handling using POST requests
* Data retrieval using GET parameters
* Redirect after form submission
* Dynamic page updates based on user input
* Conditional rendering in templates
* Basic CRUD-like operations without database
* Task state management (done / pending)
* Filtering logic using URL query parameters

⸻

🧩 Key Concepts Learned

* Difference between GET (read) and POST (send data)
* How Django processes request.method
* Importance of CSRF protection in forms
* Clean URL handling using reverse()
* Separation of logic (views) and presentation (templates)
* Why data processing should be done in Python, not templates
* Understanding user interaction flow in web applications

⸻

🚀 Result

At the end of Week 2, I can:

* Build forms that send and process user input
* Handle GET and POST requests properly
* Implement redirect patterns used in real applications
* Create interactive features like add, update, delete, and filter
* Structure backend logic for dynamic web behavior