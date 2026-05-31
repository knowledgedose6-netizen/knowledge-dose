from django.contrib import admin
from django.utils.html import format_html

from .models import (

    Category,
    Blog,
    Comment

)


# =========================================================
# BLOG ADMIN
# =========================================================

class BlogAdmin(admin.ModelAdmin):

    # =====================================================
    # AUTO SLUG
    # =====================================================

    prepopulated_fields = {

        'slug': ('title',)

    }

    # =====================================================
    # TABLE COLUMNS
    # =====================================================

    list_display = (

        'image_preview',

        'title',

        'category',

        'author',

        'status',

        'ai_badge',

        'featured_badge',

        'created_at'

    )

    # =====================================================
    # SEARCH
    # =====================================================

    search_fields = (

        'id',

        'title',

        'category__category_name',

        'status'

    )

    # =====================================================
    # FILTERS
    # =====================================================

    list_filter = (

        'status',

        'is_featured',

        'is_ai_generated',

        'category',

        'created_at'

    )

    # =====================================================
    # EDITABLE
    # =====================================================

    list_editable = (

        'status',

    )

    # =====================================================
    # ORDERING
    # =====================================================

    ordering = (

        '-created_at',

    )

    # =====================================================
    # IMAGE PREVIEW
    # =====================================================

    def image_preview(self, obj):

        if obj.featured_image:

            return format_html(

                '''

                <img
                    src="{}"
                    width="90"
                    height="70"
                    style="
                        border-radius:10px;
                        object-fit:cover;
                        border:2px solid #ddd;
                    "
                />

                ''',

                obj.featured_image.url

            )

        return "No Image"

    image_preview.short_description = "Preview"

    # =====================================================
    # AI BADGE
    # =====================================================

    def ai_badge(self, obj):

        if obj.is_ai_generated:

            return format_html(

                '''

                <span style="
                    background:#071949;
                    color:white;
                    padding:6px 12px;
                    border-radius:20px;
                    font-size:12px;
                    font-weight:bold;
                ">
                    AI BLOG
                </span>

                '''

            )

        return format_html(

            '''

            <span style="
                background:#d1fae5;
                color:#065f46;
                padding:6px 12px;
                border-radius:20px;
                font-size:12px;
                font-weight:bold;
            ">
                USER BLOG
            </span>

            '''

        )

    ai_badge.short_description = "Blog Type"

    # =====================================================
    # FEATURED BADGE
    # =====================================================

    def featured_badge(self, obj):

        if obj.is_featured:

            return format_html(

                '''

                <span style="
                    background:#facc15;
                    color:#000;
                    padding:6px 12px;
                    border-radius:20px;
                    font-size:12px;
                    font-weight:bold;
                ">
                    FEATURED
                </span>

                '''

            )

        return "-"

    featured_badge.short_description = "Featured"


# =========================================================
# CATEGORY ADMIN
# =========================================================

class CategoryAdmin(admin.ModelAdmin):

    list_display = (

        'category_name',

        'created_at'

    )

    search_fields = (

        'category_name',

    )


# =========================================================
# COMMENT ADMIN
# =========================================================

class CommentAdmin(admin.ModelAdmin):

    list_display = (

        'user',

        'blog',

        'created_at'

    )

    search_fields = (

        'user__username',

        'blog__title',

        'comment'

    )

    ordering = (

        '-created_at',

    )


# =========================================================
# REGISTER
# =========================================================

admin.site.register(

    Category,

    CategoryAdmin

)

admin.site.register(

    Blog,

    BlogAdmin

)

admin.site.register(

    Comment,

    CommentAdmin

)