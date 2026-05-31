from django.db import models

from django.contrib.auth.models import User

from django.utils.text import slugify

from ckeditor.fields import RichTextField


# ================= CATEGORY ================= #

class Category(models.Model):

    category_name = models.CharField(
        max_length=50,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        verbose_name_plural = 'categories'

    def __str__(self):

        return self.category_name


# ================= STATUS ================= #

STATUS_CHOICES = (

    ("Draft", "Draft"),

    ("Published", "Published")

)


# ================= BLOG ================= #

class Blog(models.Model):

    title = models.CharField(
        max_length=100
    )

    slug = models.SlugField(

        max_length=150,

        unique=True,

        blank=True

    )

    category = models.ForeignKey(

        Category,

        on_delete=models.CASCADE

    )

    author = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    featured_image = models.ImageField(

        upload_to='uploads/%Y/%m/%d',

        null=True,

        blank=True

    )

    short_description = models.TextField(
        max_length=500
    )

    blog_body = RichTextField()

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="Draft"

    )

    is_featured = models.BooleanField(
        default=False
    )
    
    is_ai_generated = models.BooleanField(
    default=False
    )
    

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.title


    # ✅ SAFE IMAGE URL

    @property
    def image_url(self):

        if self.featured_image:

            return self.featured_image.url

        return '/static/chatbot/images/default-ai.jpg'


    # ✅ AUTO SLUG GENERATION

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(
                self.title
            )

            slug = base_slug

            counter = 1

            while Blog.objects.filter(
                slug=slug
            ).exists():

                slug = f"{base_slug}-{counter}"

                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


# ================= COMMENT ================= #

class Comment(models.Model):

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    blog = models.ForeignKey(

        Blog,

        on_delete=models.CASCADE

    )

    comment = models.TextField(
        max_length=250
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.comment