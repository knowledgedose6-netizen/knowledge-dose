# =========================================================
# KD AI ASSISTANT - models.py
# FULLY UPGRADED ULTRA PREMIUM VERSION
# =========================================================

from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string


# =========================================================
# CHAT HISTORY MODEL
# =========================================================

class ChatHistory(models.Model):

    STATUS_CHOICES = (

        ("draft", "Draft"),

        ("published", "Published")

    )

    title = models.CharField(

        max_length=255

    )

    slug = models.SlugField(

        unique=True,

        blank=True,

        null=True

    )

    category = models.CharField(

        max_length=120,

        default="General"

    )

    prompt = models.TextField()

    content = models.TextField()

    faq = models.TextField(

        blank=True,

        null=True

    )

    conclusion = models.TextField(

        blank=True,

        null=True

    )

    tags = models.CharField(

        max_length=500,

        blank=True,

        null=True

    )

    featured_image = models.URLField(

        blank=True,

        null=True

    )

    seo_score = models.IntegerField(

        default=95

    )

    grammar_score = models.IntegerField(

        default=95

    )

    tone = models.CharField(

        max_length=120,

        default="Professional"

    )

    # =====================================================
    # NEW FIELDS
    # =====================================================

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="published"

    )

    is_featured = models.BooleanField(

        default=False

    )

    views = models.PositiveIntegerField(

        default=0

    )

    likes = models.PositiveIntegerField(

        default=0

    )

    shares = models.PositiveIntegerField(

        default=0

    )

    youtube_links = models.JSONField(

        default=list,

        blank=True

    )

    image_gallery = models.JSONField(

        default=list,

        blank=True

    )

    reading_time = models.CharField(

        max_length=50,

        default="5 min read"

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    class Meta:

        ordering = [

            "-created_at"

        ]

        verbose_name = "AI Blog"

        verbose_name_plural = "AI Blogs"

    # =====================================================
    # AUTO SLUG
    # =====================================================

    def generate_unique_slug(self):

        base_slug = slugify(
            self.title
        )

        slug = base_slug

        counter = 1

        while ChatHistory.objects.filter(
            slug=slug
        ).exclude(
            id=self.id
        ).exists():

            slug = (
                f"{base_slug}-{counter}"
            )

            counter += 1

        return slug

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = (
                self.generate_unique_slug()
            )

        if not self.reading_time:

            word_count = len(
                self.content.split()
            )

            minutes = max(
                1,
                round(word_count / 200)
            )

            self.reading_time = (
                f"{minutes} min read"
            )

        super().save(
            *args,
            **kwargs
        )

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return self.title


# =========================================================
# SAVED DRAFT MODEL
# =========================================================

class SavedDraft(models.Model):

    title = models.CharField(

        max_length=255

    )

    prompt = models.TextField()

    content = models.TextField()

    category = models.CharField(

        max_length=100,

        default="General"

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    class Meta:

        ordering = [

            "-created_at"

        ]

    def __str__(self):

        return self.title


# =========================================================
# TRENDING BLOG MODEL
# =========================================================

class TrendingBlog(models.Model):

    title = models.CharField(

        max_length=255

    )

    category = models.CharField(

        max_length=100

    )

    image = models.URLField(

        blank=True,

        null=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = [

            "-created_at"

        ]

    def __str__(self):

        return self.title


# =========================================================
# BLOG ANALYTICS
# =========================================================

class BlogAnalytics(models.Model):

    blog = models.ForeignKey(

        ChatHistory,

        on_delete=models.CASCADE,

        related_name="analytics"

    )

    views = models.IntegerField(

        default=0

    )

    likes = models.IntegerField(

        default=0

    )

    shares = models.IntegerField(

        default=0

    )

    reading_time = models.CharField(

        max_length=50,

        default="5 min read"

    )

    engagement_score = models.IntegerField(

        default=90

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = [

            "-created_at"

        ]

    def __str__(self):

        return f"{self.blog.title} Analytics"


# =========================================================
# USER FEEDBACK
# =========================================================

class UserFeedback(models.Model):

    blog = models.ForeignKey(

        ChatHistory,

        on_delete=models.CASCADE

    )

    rating = models.IntegerField(

        default=5

    )

    feedback = models.TextField(

        blank=True,

        null=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    class Meta:

        ordering = [

            "-created_at"

        ]

    def __str__(self):

        return f"{self.blog.title} Feedback"


# =========================================================
# AI SETTINGS MODEL
# =========================================================

class AISettings(models.Model):

    ai_name = models.CharField(

        max_length=100,

        default="KD AI"

    )

    ai_voice = models.CharField(

        max_length=100,

        default="en-US"

    )

    ai_theme = models.CharField(

        max_length=100,

        default="Premium Blue"

    )

    enable_voice = models.BooleanField(

        default=True

    )

    enable_youtube = models.BooleanField(

        default=True

    )

    enable_images = models.BooleanField(

        default=True

    )

    enable_seo = models.BooleanField(

        default=True

    )

    enable_humanizer = models.BooleanField(

        default=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    def __str__(self):

        return self.ai_name