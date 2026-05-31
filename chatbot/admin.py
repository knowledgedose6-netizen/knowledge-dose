# =========================================================
# KD AI ASSISTANT - admin.py
# FULLY UPGRADED ULTRA PREMIUM ADMIN PANEL
# =========================================================

from django.contrib import admin
from django.utils.html import format_html

from .models import (

    ChatHistory,
    SavedDraft,
    TrendingBlog,
    BlogAnalytics,
    UserFeedback,
    AISettings

)


# =========================================================
# ADMIN SITE CUSTOMIZATION
# =========================================================

admin.site.site_header = (
    "KD AI ADMIN PANEL"
)

admin.site.site_title = (
    "KD AI ADMIN"
)

admin.site.index_title = (
    "Welcome To KD AI Dashboard"
)


# =========================================================
# CHAT HISTORY ADMIN
# =========================================================

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):

    list_display = (

        "title",

        "category",

        "status",

        "is_featured",

        "seo_score",

        "grammar_score",

        "views",

        "created_at"

    )

    search_fields = (

        "title",

        "category",

        "content",

        "tags"

    )

    list_filter = (

        "category",

        "status",

        "is_featured",

        "created_at"

    )

    prepopulated_fields = {

        "slug":("title",)

    }

    readonly_fields = (

        "created_at",

        "updated_at",

        "featured_image_preview",
        
        "gallery_preview",

        "youtube_preview",

    )

    ordering = (

        "-created_at",

    )

    list_per_page = 20

    actions = [

        "publish_blogs",

        "draft_blogs",

        "mark_featured",

        "remove_featured"

    ]

    fieldsets = (

        (

            "Blog Information",

            {

                "fields":(

                    "title",

                    "slug",

                    "category",

                    "status",

                    "is_featured"

                )

            }

        ),

        (

            "AI Content",

            {

                "fields":(

                    "prompt",

                    "content",

                    "faq",

                    "conclusion",

                    "tags"

                )

            }

        ),

        (

            "Media",

            {

                "fields":(

                    "featured_image",

                    "featured_image_preview",
                    
                    "gallery_preview",

                    "image_gallery",
                    
                    "youtube_preview",

                    "youtube_links"

                )

            }

        ),

        (

            "SEO & Analytics",

            {

                "fields":(

                    "seo_score",

                    "grammar_score",

                    "reading_time",

                    "views",

                    "likes",

                    "shares",

                    "tone"

                )

            }

        ),

        (

            "Timestamps",

            {

                "fields":(

                    "created_at",

                    "updated_at"

                )

            }

        )

    )

    # =====================================================
    # IMAGE PREVIEW
    # =====================================================

    def featured_image_preview(self, obj):

        if obj.featured_image:

            return format_html(

                """

                <img
                    src="{}"
                    width="200"
                    style="
                        border-radius:15px;
                        object-fit:cover;
                        border:2px solid #ddd;
                    "
                >

                """,

                obj.featured_image

            )

        return "No Image"

    featured_image_preview.short_description = (
        "Featured Image Preview"
    ) 
    # =====================================================
    # GALLERY PREVIEW
    # =====================================================

    def gallery_preview(self, obj):

        if not obj.image_gallery:

            return "No Gallery Images"

        images_html = ""

        try:

            for image in obj.image_gallery[:4]:

                images_html += f"""

                <img
                    src="{image}"
                    width="120"
                    height="90"
                    style="
                        margin:8px;
                        border-radius:12px;
                        object-fit:cover;
                        border:2px solid #ddd;
                    "
                >

                """

            return format_html(images_html)

        except Exception:

            return "Gallery Preview Error"

    gallery_preview.short_description = (
        "Gallery Preview"
    )


    # =====================================================
    # YOUTUBE PREVIEW
    # =====================================================

    def youtube_preview(self, obj):

        if not obj.youtube_links:

            return "No Videos"

        videos_html = ""

        try:

            for video in obj.youtube_links[:3]:

                thumbnail = video.get(
                    "thumbnail"
                )

                title = video.get(
                    "title"
                )

                videos_html += f"""

                <div style="
                    display:inline-block;
                    margin:10px;
                    text-align:center;
                ">

                    <img
                        src="{thumbnail}"
                        width="180"
                        height="100"
                        style="
                            border-radius:12px;
                            object-fit:cover;
                            border:2px solid #ddd;
                            display:block;
                            margin-bottom:8px;
                        "
                    >

                    <small
                        style="
                            display:block;
                            width:180px;
                            font-weight:600;
                        "
                    >
                        {title}
                    </small>

                </div>

                """

            return format_html(videos_html)

        except Exception:

            return "Video Preview Error"

    youtube_preview.short_description = (
        "YouTube Preview"
    )

    # =====================================================
    # BULK ACTIONS
    # =====================================================

    def publish_blogs(

        self,

        request,

        queryset

    ):

        queryset.update(
            status="published"
        )

    publish_blogs.short_description = (
        "Publish Selected Blogs"
    )

    def draft_blogs(

        self,

        request,

        queryset

    ):

        queryset.update(
            status="draft"
        )

    draft_blogs.short_description = (
        "Move Selected Blogs To Draft"
    )

    def mark_featured(

        self,

        request,

        queryset

    ):

        queryset.update(
            is_featured=True
        )

    mark_featured.short_description = (
        "Mark Selected Blogs As Featured"
    )

    def remove_featured(

        self,

        request,

        queryset

    ):

        queryset.update(
            is_featured=False
        )

    remove_featured.short_description = (
        "Remove Featured From Selected Blogs"
    )


# =========================================================
# SAVED DRAFT ADMIN
# =========================================================

@admin.register(SavedDraft)
class SavedDraftAdmin(admin.ModelAdmin):

    list_display = (

        "title",

        "category",

        "created_at",

        "updated_at"

    )

    search_fields = (

        "title",

        "content"

    )

    list_filter = (

        "category",

    )

    ordering = (

        "-created_at",

    )

    list_per_page = 20


# =========================================================
# TRENDING BLOG ADMIN
# =========================================================

@admin.register(TrendingBlog)
class TrendingBlogAdmin(admin.ModelAdmin):

    list_display = (

        "title",

        "category",

        "created_at"

    )

    search_fields = (

        "title",

    )

    list_filter = (

        "category",

    )

    ordering = (

        "-created_at",

    )

    list_per_page = 20


# =========================================================
# BLOG ANALYTICS ADMIN
# =========================================================

@admin.register(BlogAnalytics)
class BlogAnalyticsAdmin(admin.ModelAdmin):

    list_display = (

        "blog",

        "views",

        "likes",

        "shares",

        "engagement_score",

        "created_at"

    )

    search_fields = (

        "blog__title",

    )

    ordering = (

        "-created_at",

    )

    list_per_page = 20


# =========================================================
# USER FEEDBACK ADMIN
# =========================================================

@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):

    list_display = (

        "blog",

        "rating",

        "created_at"

    )

    search_fields = (

        "blog__title",

        "feedback"

    )

    list_filter = (

        "rating",

    )

    ordering = (

        "-created_at",

    )

    list_per_page = 20


# =========================================================
# AI SETTINGS ADMIN
# =========================================================

@admin.register(AISettings)
class AISettingsAdmin(admin.ModelAdmin):

    list_display = (

        "ai_name",

        "ai_voice",

        "ai_theme",

        "enable_voice",

        "enable_youtube",

        "enable_images",

        "enable_seo",

        "enable_humanizer"

    )

    list_editable = (

        "enable_voice",

        "enable_youtube",

        "enable_images",

        "enable_seo",

        "enable_humanizer"

    )

    list_per_page = 10