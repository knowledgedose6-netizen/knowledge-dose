from django.urls import path

from . import views


urlpatterns = [

    # CHATBOT PAGE

    path(

        'kd-ai/',

        views.chatbot_page,

        name='chatbot_page'

    ),

    # GENERATE BLOG

    path(

        'generate-blog/',

        views.generate_blog,

        name='generate_blog'

    ),

    # SAVE DRAFT

    path(

        'save-draft/',

        views.save_draft,

        name='save_draft'

    ),

    # REWRITE CONTENT

    path(

        'rewrite-blog/',

        views.rewrite_blog,

        name='rewrite_blog'

    ),

    # SEO IMPROVEMENT

    path(

        'seo-blog/',

        views.seo_blog,

        name='seo_blog'

    ),

    # HUMANIZE CONTENT

    path(

        'humanize-blog/',

        views.humanize_blog,

        name='humanize_blog'

    ),

    # GRAMMAR FIX

    path(

        'grammar-blog/',

        views.grammar_blog,

        name='grammar_blog'

    ),

    # CHAT HISTORY

    path(

        'chat-history/',

        views.get_chat_history,

        name='chat_history'

    ),

]