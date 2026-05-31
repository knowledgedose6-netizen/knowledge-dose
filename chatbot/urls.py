# =========================================================
# KD AI ASSISTANT - urls.py
# ULTRA PREMIUM URLS
# =========================================================

from django.urls import path

from . import views


urlpatterns = [

    # =====================================================
    # CHATBOT PAGE
    # =====================================================

    path(

        "",

        views.chatbot_page,

        name="chatbot"

    ),

    # =====================================================
    # GENERATE BLOG
    # =====================================================

    path(

        "generate-blog/",

        views.generate_blog,

        name="generate_blog"

    ),

    # =====================================================
    # SAVE BLOG
    # =====================================================

    path(

        "save-blog/",

        views.save_blog,

        name="save_blog"

    ),

    # =====================================================
    # REWRITE BLOG
    # =====================================================

    path(

        "rewrite-blog/",

        views.rewrite_blog,

        name="rewrite_blog"

    ),

    # =====================================================
    # SEO CHECK
    # =====================================================

    path(

        "seo-check/",

        views.seo_check,

        name="seo_check"

    ),

    # =====================================================
    # GRAMMAR API
    # =====================================================

    path(

        "grammar-api/",

        views.grammar_api,

        name="grammar_api"

    ),

    # =====================================================
    # TRENDING BLOGS
    # =====================================================

    path(

        "trending-blogs/",

        views.trending_blogs,

        name="trending_blogs"

    ),

    # =====================================================
    # YOUTUBE TEST
    # =====================================================

    path(

        "youtube-test/",

        views.youtube_test,

        name="youtube_test"

    ),

]