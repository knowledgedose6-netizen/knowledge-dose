from django import forms
from blogs.models import Blog, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SiteSettings

class CategoryForm(forms.ModelForm):
    
    class Meta:

        model = Category

        fields = '__all__'

        widgets = {

            'category_name': forms.TextInput(
                attrs={
                    'class': 'kdose-input',
                    'placeholder': 'Enter category name'
                }
            )

        }



class BlogPostForm(forms.ModelForm):

    class Meta:

        model = Blog

        fields = (
            'title',
            'category',
            'featured_image',
            'short_description',
            'blog_body',
            'status',
            'is_featured'
        )

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'kdose-input',
                    'placeholder': 'Enter blog title'
                }
            ),

            'category': forms.Select(
                attrs={
                    'class': 'kdose-select'
                }
            ),

            'featured_image': forms.FileInput(
                attrs={
                    'class': 'kdose-file'
                }
            ),

            'short_description': forms.Textarea(
                attrs={
                    'class': 'kdose-textarea',
                    'rows': 4,
                    'placeholder': 'Short description'
                }
            ),

            'status': forms.Select(
                attrs={
                    'class': 'kdose-select'
                }
            ),

        }




class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

class SiteSettingsForm(forms.ModelForm):

    class Meta:
        model = SiteSettings

        fields = '__all__'