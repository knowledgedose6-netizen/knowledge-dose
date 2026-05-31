
from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),
    path(
    'posts/',
    views.posts,
    name='posts'
),
    path(
    'add-post/',
    views.add_post,
    name='add_post'
),
    path(
    'edit-post/<int:id>/',
    views.edit_post,
    name='edit_post'
),
    path(
    'draft-posts/',
    views.draft_posts,
    name='draft_posts'
),
    path(
    'delete-post/<int:id>/',
    views.delete_post,
    name='delete_post'
),

path(
    'featured-posts/',
    views.featured_posts,
    name='featured_posts'
),
path(
    'categories/',
    views.categories,
    name='categories'
),

path(
    'add-category/',
    views.add_category,
    name='add_category'
),

path(
    'edit-category/<int:id>/',
    views.edit_category,
    name='edit_category'
),

path(
    'delete-category/<int:id>/',
    views.delete_category,
    name='delete_category'
),
    
    path(
    'comments/',
    views.comments,
    name='comments'
),
    path(
    'delete-comment/<int:id>/',
    views.delete_comment,
    name='delete_comment'
),
    path(
    'users/',
    views.users,
    name='users'
),

path(
    'add-user/',
    views.add_user,
    name='add_user'
),

path(
    'edit-user/<int:id>/',
    views.edit_user,
    name='edit_user'
),

path(
    'delete-user/<int:id>/',
    views.delete_user,
    name='delete_user'
),
path(
    'ai-tools/',
    views.ai_tools,
    name='ai_tools'
),



path(
    'content-rewriter/',
    views.content_rewriter,
    name='content_rewriter'
),

path(
    'ai-assistant/',
    views.ai_assistant,
    name='ai_assistant'
),
path(
    'ai-blog-generator/',
    views.ai_blog_generator,
    name='ai_blog_generator'
),
path(
    'seo-generator/',
    views.seo_generator,
    name='seo_generator'
),
path(
    'daily-report/',
    views.daily_report,
    name='daily_report'
),

path(
    'weekly-report/',
    views.weekly_report,
    name='weekly_report'
),

path(
    'monthly-report/',
    views.monthly_report,
    name='monthly_report'
),

path(
    'yearly-report/',
    views.yearly_report,
    name='yearly_report'
),
]


