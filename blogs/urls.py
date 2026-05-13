from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    # ================= SAVE BLOG =================

    path(
        'save-blog/',
        views.save_blog,
        name='save_blog'
    ),

    # ================= AUTOSAVE =================

    path(
        'autosave/',
        views.autosave_blog,
        name='autosave_blog'
    ),

    # ================= GRAMMAR =================

    path(
        'grammar/',
        views.grammar_check,
        name='grammar_check'
    ),

    # ================= TONE =================

    path(
        'tone/',
        views.tone_check,
        name='tone_check'
    ),

    # ================= CKEDITOR =================

    path(
        'ckeditor/',
        include('ckeditor_uploader.urls')
    ),

    # ================= BLOG DETAIL =================

    path(
        'blog/<slug:slug>/',
        views.blogs,
        name='blog_detail'
    ),

    # ================= CATEGORY =================

    path(
        '<int:category_id>/',
        views.posts_by_category,
        name='posts_by_category'
    ),

] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)