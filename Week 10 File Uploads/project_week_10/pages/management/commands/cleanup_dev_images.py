from django.core.management.base import BaseCommand
from django.conf import settings
from pages.models import DevBlog

class Command(BaseCommand):
    help = "Delete unused blog images from media/dev_blog_images."

    def handle(self, *args, **kwargs):
        used_images = set(
            DevBlog.objects
            .exclude(cover_image="")
            .exclude(cover_image__isnull=True)
            .values_list("cover_image", flat=True)
        )
        blog_images_dir=settings.MEDIA_ROOT / "dev_blog_images"

        if not blog_images_dir.exists():
            self.stdout.write("No dev_blog_images folder found.")
            return
        
        delete_count = 0

        for file_path in blog_images_dir.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(settings.MEDIA_ROOT)
            
                if str(relative_path) not in used_images:
                    file_path.unlink()
                    delete_count += 1
                    self.stdout.write(f"Delete: {relative_path}")
        self.stdout.write(
            self.style.SUCCESS(f"Cleanup finished. Deleted {delete_count} files.")
        )