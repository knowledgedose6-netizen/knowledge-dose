"""
URL configuration for blog_main project.
"""

from django.contrib import admin

from django.urls import (

    path,

    include

)

from django.conf import settings

from django.conf.urls.static import static

from . import views

from blogs import views as BlogsView


urlpatterns = [

    # ADMIN

    path(

        'admin/',

        admin.site.urls

    ),

    # HOME

    path(

        '',

        views.home,

        name='home'

    ),

    # BLOG CATEGORIES

    path(

        'category/',

        include('blogs.urls')

    ),

    # BLOG DETAILS

    path(

        'blogs/<slug:slug>/',

        BlogsView.blogs,

        name='blogs'

    ),

    # SEARCH

    path(

        'search/',

        BlogsView.search,

        name='search'

    ),

    # AUTHENTICATION

    path(

        'register/',

        views.register,

        name='register'

    ),

    path(

        'login/',

        views.login,

        name='login'

    ),

    path(

        'logout/',

        views.logout,

        name='logout'

    ),

    # SIMPLE EDITOR

    path(

        'write/',

        views.editor_page,

        name='editor_page'

    ),

    # CKEDITOR

    path(

        'ckeditor/',

        include('ckeditor_uploader.urls')

    ),

    # CHATBOT

    path(

        'chatbot/',

        include('chatbot.urls')

    ),

    # DASHBOARD

    path(

        'dashboard/',

        include('dashboards.urls')

    ),

]


# MEDIA FILES

if settings.DEBUG:

    urlpatterns += static(

        settings.MEDIA_URL,

        document_root=settings.MEDIA_ROOT

    )