from django.contrib import admin

from django.utils.html import format_html

from django.core.files import File

from urllib.request import urlopen

from tempfile import NamedTemporaryFile


from .models import (

    AIBlogDraft,

    ChatHistory,

    AIImage,

    AIChatMessage

)

from blogs.models import Blog, Category


# ================= AI BLOG DRAFT ADMIN ================= #

@admin.register(AIBlogDraft)
class AIBlogDraftAdmin(admin.ModelAdmin):

    list_display = (

        'title',

        'category',

        'seo_score',

        'grammar_score',

        'tone',

        'publish_requested',

        'is_published',

        'is_featured',

        'image_preview',

        'created_at'

    )

    search_fields = (

        'title',

        'category',

        'tags',

        'content'

    )

    list_filter = (

        'is_published',

        'publish_requested',

        'is_featured',

        'category',

        'tone'

    )

    prepopulated_fields = {

        'slug': ('title',)

    }

    readonly_fields = (

        'created_at',

        'updated_at',

        'published_at',

        'image_preview'

    )


    # ✅ ADMIN IMAGE PREVIEW

    def image_preview(self, obj):

        if obj.featured_image_url:

            return format_html(

                '<img src="{}" width="120" style="border-radius:10px;" />',

                obj.featured_image_url

            )

        return "No Image"

    image_preview.short_description = "Preview"


    # ✅ AUTO PUBLISH TO BLOG MODEL

    def save_model(

        self,

        request,

        obj,

        form,

        change

    ):

        super().save_model(

            request,

            obj,

            form,

            change

        )

        # ✅ ONLY WHEN PUBLISHED

        if obj.is_published:

            category_obj, created = Category.objects.get_or_create(

                category_name=obj.category

            )

            # ✅ AVOID DUPLICATE BLOGS

            if not Blog.objects.filter(

                title=obj.title

            ).exists():

                blog = Blog.objects.create(

                    title=obj.title,

                    category=category_obj,

                    author=request.user,

                    short_description=obj.meta_description,

                    blog_body=obj.content,

                    status='Published',

                    is_featured=obj.is_featured

                )

                # ✅ ATTACH AI IMAGE

                if obj.featured_image_url:

                    try:

                        image_url = obj.featured_image_url

                        # ✅ ABSOLUTE URL FIX

                        if image_url.startswith('/'):

                            image_url = request.build_absolute_uri(
                                image_url
                            )

                        img_temp = NamedTemporaryFile(delete=True)

                        img_temp.write(

                            urlopen(image_url).read()

                        )

                        img_temp.flush()

                        # ✅ SAVE IMAGE TO BLOG MODEL

                        blog.featured_image.save(

                            f"{obj.slug}.webp",

                            File(img_temp),

                            save=True

                        )

                    except Exception as e:

                        print("IMAGE ERROR:", e)


# ================= CHAT HISTORY ADMIN ================= #

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):

    list_display = (

        'user',

        'created_at'

    )

    search_fields = (

        'user__username',

        'user_message'

    )

    readonly_fields = (

        'created_at',

    )


# ================= AI IMAGE ADMIN ================= #

@admin.register(AIImage)
class AIImageAdmin(admin.ModelAdmin):

    list_display = (

        'alt_text',

        'draft',

        'created_at'

    )

    search_fields = (

        'alt_text',

    )

    readonly_fields = (

        'created_at',

    )


# ================= AI CHAT ADMIN ================= #

@admin.register(AIChatMessage)
class AIChatMessageAdmin(admin.ModelAdmin):

    list_display = (

        'user',

        'chat_title',

        'created_at'

    )

    search_fields = (

        'chat_title',

        'message'

    )

    readonly_fields = (

        'created_at',

    )