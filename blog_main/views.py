from django.shortcuts import redirect, render

from blogs.models import Blog, Category
from assignments.models import About
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

# 🔥 NEW IMPORT
from django.contrib.auth.decorators import login_required

# 🔥 NEW IMPORT (slug ke liye)
from django.utils.text import slugify


def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('updated_at')
    posts = Blog.objects.filter(is_featured=False, status='Published')
    
     # Fetch about us
    try:
        about = About.objects.get()
    except:
        about = None   
    context = {
        'featured_posts': featured_posts,
        'posts': posts,
        'about': about,
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


# ❗ UPDATED LOGIN FUNCTION (same as yours ✔)
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('editor_page')  # ✔ already correct

    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')


# 🔥 UPDATED VIEW: EDITOR PAGE (SAVE DRAFT ADDED)
@login_required
def editor_page(request):

    categories = Category.objects.all()  # 🔥 NEW

    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        short_description = request.POST.get('short_description')
        blog_body = request.POST.get('blog_body')
        image = request.FILES.get('featured_image')

        # 🔥 SAFE CATEGORY FETCH
        try:
            category = Category.objects.get(id=category_id)
        except:
            category = Category.objects.first()

        # 🔥 CREATE BLOG (DRAFT)
        Blog.objects.create(
            title=title,
            slug=slugify(title),
            category=category,
            author=request.user,
            featured_image=image,
            short_description=short_description,
            blog_body=blog_body,
            status="Draft"   # 🔥 IMPORTANT
        )

        return redirect('editor_page')

    return render(request, 'editor.html', {'categories': categories})