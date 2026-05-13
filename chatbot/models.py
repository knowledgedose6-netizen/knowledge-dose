from django.db import models

from django.contrib.auth.models import User


class AIBlogDraft(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ai_drafts',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=300
    )

    slug = models.SlugField(
        unique=True
    )

    category = models.CharField(
        max_length=100
    )

    meta_description = models.TextField()

    tags = models.CharField(
        max_length=300
    )

    content = models.TextField()

    featured_image = models.ImageField(
        upload_to='ai_blogs/',
        blank=True,
        null=True
    )

    featured_image_url = models.URLField(
        blank=True,
        null=True
    )

    faq = models.TextField(
        blank=True
    )

    conclusion = models.TextField(
        blank=True
    )

    admin_feedback = models.TextField(
        blank=True
    )

    publish_requested = models.BooleanField(
        default=False
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True
    )

    ai_prompt = models.TextField(
        default='AI Blog Prompt'
    )

    seo_score = models.IntegerField(
        default=0
    )

    grammar_score = models.IntegerField(
        default=0
    )

    readability_score = models.IntegerField(
        default=0
    )

    tone = models.CharField(
        max_length=100,
        blank=True
    )

    ai_model = models.CharField(
        max_length=100,
        default='Gemini'
    )

    is_published = models.BooleanField(
        default=False
    )

    is_featured = models.BooleanField(
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


class ChatHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    user_message = models.TextField()

    ai_response = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        if self.user:

            return f'{self.user.username} Chat'

        return 'Anonymous Chat'


class AIImage(models.Model):

    draft = models.ForeignKey(
        AIBlogDraft,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='ai_blogs/'
    )

    alt_text = models.CharField(
        max_length=300
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.alt_text


class AIChatMessage(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    chat_title = models.CharField(
        max_length=300,
        blank=True
    )

    message = models.TextField()

    response = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.message[:50]