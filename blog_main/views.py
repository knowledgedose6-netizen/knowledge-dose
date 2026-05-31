from django.shortcuts import (

    redirect,

    render

)

from django.contrib import auth

from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import AuthenticationForm

from django.utils.text import slugify

from blogs.models import (

    Blog,

    Category

)

from assignments.models import About

from .forms import RegistrationForm


# =========================
# HOME
# =========================

def home(request):

    # =========================================
    # FEATURED POSTS
    # =========================================

    featured_posts = Blog.objects.filter(

        is_featured=True,

        status='Published'

    ).order_by('-updated_at')

    # =========================================
    # NORMAL POSTS
    # =========================================

    posts = Blog.objects.filter(

        is_featured=False,

        status='Published'

    ).order_by('-updated_at')

    # =========================================
    # ABOUT SECTION
    # =========================================

    try:

        about = About.objects.get()

    except About.DoesNotExist:

        about = None

    # =========================================
    # AI BLOGS SUPPORT
    # =========================================

    from chatbot.models import ChatHistory

    ai_featured_posts = (

        ChatHistory.objects.filter(

            status='published',

            is_featured=True

        )

        .order_by('-created_at')

    )

    ai_posts = (

        ChatHistory.objects.filter(

            status='published',

            is_featured=False

        )

        .order_by('-created_at')

    )

    # =========================================
    # CONTEXT
    # =========================================

    context = {

        'featured_posts':
        featured_posts,

        'posts':
        posts,

        'about':
        about,

        # =====================================
        # AI BLOGS
        # =====================================

        'ai_featured_posts':
        ai_featured_posts,

        'ai_posts':
        ai_posts,

    }

    return render(

        request,

        'home.html',

        context

    )


# =========================
# REGISTER
# =========================

def register(request):

    if request.method == 'POST':

        form = RegistrationForm(

            request.POST

        )

        if form.is_valid():

            form.save()

            return redirect(

                'login'

            )

    else:

        form = RegistrationForm()

    return render(

        request,

        'register.html',

        {

            'form': form

        }

    )


# =========================
# LOGIN
# =========================

def login(request):

    if request.method == 'POST':

        form = AuthenticationForm(

            request,

            request.POST

        )

        if form.is_valid():

            username = form.cleaned_data[
                'username'
            ]

            password = form.cleaned_data[
                'password'
            ]

            user = auth.authenticate(

                username=username,

                password=password

            )

            if user is not None:

                auth.login(

                    request,

                    user

                )

                # REDIRECT TO KD AI

                return redirect(

                    'chatbot_page'

                )

    else:

        form = AuthenticationForm()

    return render(

        request,

        'login.html',

        {

            'form': form

        }

    )


# =========================
# LOGOUT
# =========================

def logout(request):

    auth.logout(request)

    return redirect(

        'home'

    )


# =========================
# SIMPLE BLOG EDITOR
# =========================

@login_required(

    login_url='login'

)

def editor_page(request):

    categories = Category.objects.all()

    if request.method == 'POST':

        title = request.POST.get(
            'title'
        )

        category_id = request.POST.get(
            'category'
        )

        short_description = request.POST.get(
            'short_description'
        )

        blog_body = request.POST.get(
            'blog_body'
        )

        featured_image = request.FILES.get(
            'featured_image'
        )

        # =====================================
        # VALIDATION
        # =====================================

        if not title or not blog_body:

            return render(

                request,

                'editor.html',

                {

                    'categories':
                    categories,

                    'error':
                    'Title and Blog Body required'

                }

            )

        # =====================================
        # CATEGORY
        # =====================================

        try:

            category = Category.objects.get(

                id=category_id

            )

        except Category.DoesNotExist:

            category = Category.objects.first()

        # =====================================
        # UNIQUE SLUG
        # =====================================

        base_slug = slugify(
            title
        )

        slug = base_slug

        counter = 1

        while Blog.objects.filter(
            slug=slug
        ).exists():

            slug = f'{base_slug}-{counter}'

            counter += 1

        # =====================================
        # SAVE BLOG
        # =====================================

        Blog.objects.create(

            title=title,

            slug=slug,

            category=category,

            author=request.user,

            featured_image=featured_image,

            short_description=
            short_description,

            blog_body=blog_body,

            # =================================
            # IMPORTANT FIX
            # =================================

            status='Published'

        )

        return render(

            request,

            'editor.html',

            {

                'categories':
                categories,

                'success':
                'Blog Published Successfully ✅'

            }

        )

    return render(

        request,

        'editor.html',

        {

            'categories':
            categories

        }

    )