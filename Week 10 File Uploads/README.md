## Week 10 — Django File Uploads

In Week 10, I focused on learning how Django handles uploaded files and images, including how files are stored, displayed, processed, replaced, and cleaned up.

Throughout the week, I added image upload functionality to blog-style applications, configured media settings, used ModelForms with file inputs, processed images with Pillow, supported HEIC uploads, and built cleanup logic to prevent unused files from remaining in the media folder.

Key skills developed:

* Understanding the difference between:
    * static files
    * media files
* Configuring uploaded media using:
    * MEDIA_ROOT
    * MEDIA_URL
* Understanding that uploaded files are stored on disk while the database stores only the file path
* Using model fields for uploads:
    * FileField
    * ImageField
* Installing and using:
    * Pillow
    * pillow-heif
* Understanding upload_to:
    * simple folder paths
    * custom upload path functions
    * user-specific upload folders
    * UUID-based filenames
* Building reusable image upload forms using:
    * ModelForm
    * ClearableFileInput
    * accept attributes
* Understanding why file upload forms require:
    * enctype="multipart/form-data"
* Processing uploaded files with:
    * request.POST
    * request.FILES
* Using CBVs with file uploads:
    * CreateView
    * UpdateView
    * DeleteView
* Understanding that CreateView automatically handles request.FILES when the form and template are configured correctly
* Displaying uploaded images in templates using:
    * image.url
    * image.name
    * image.path
    * image.size
* Safely displaying optional images using:
    * {% if object.image %}
* Adding image previews on edit pages using reusable context variables
* Understanding image replacement behavior:
    * no new image selected keeps the old image
    * new image selected replaces the database path
    * clear checkbox removes the database reference
* Understanding orphan files and why Django does not delete old files automatically
* Overriding model methods:
    * save()
    * delete()
* Deleting old images when replacing or clearing uploaded files
* Deleting uploaded images when deleting model objects
* Creating custom management commands to clean existing orphan files
* Using recursive file searching with:
    * rglob()
* Processing images with Pillow:
    * opening images
    * reading width and height
    * reading image format
    * reading image mode
    * resizing with thumbnail()
    * preserving aspect ratio
    * saving optimized images
* Understanding the difference between:
    * resizing
    * compressing
    * converting
* Understanding image modes:
    * RGB
    * RGBA
    * P
* Understanding why JPEG requires RGB
* Supporting HEIC / HEIF uploads with:
    * register_heif_opener()
* Converting HEIC / HEIF images into web-friendly JPG files
* Understanding the difference between:
    * .jpg / .jpeg file extensions
    * JPEG image format
* Using quality and optimize options when saving images
* Avoiding unnecessary image conversion when the original format should be preserved
* Creating a project .gitignore file to exclude:
    * media/
    * db.sqlite3
    * virtual environments
    * environment variables
    * cache files
    * logs
* Building a Week 10 project using:
    * image upload model
    * list view
    * detail view
    * create view
    * update view
    * delete view
    * reusable form template
    * reusable delete template
    * uploaded image cleanup
    * basic CSS styling

This week marked the transition from storing only text-based database content to handling real user-uploaded files. I learned how Django connects uploaded files, database paths, media settings, forms, templates, image processing, and cleanup logic into one complete file upload system suitable for more realistic web applications.