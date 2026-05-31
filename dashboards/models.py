from django.db import models


class SiteSettings(models.Model):

    site_name = models.CharField(max_length=200)

    site_logo = models.ImageField(upload_to='settings/')

    favicon = models.ImageField(upload_to='settings/')

    contact_email = models.EmailField()

    footer_text = models.TextField()

    facebook = models.URLField(blank=True, null=True)

    instagram = models.URLField(blank=True, null=True)

    twitter = models.URLField(blank=True, null=True)

    youtube = models.URLField(blank=True, null=True)

    meta_title = models.CharField(max_length=255)

    meta_description = models.TextField()

    maintenance_mode = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name


class BlogAnalytics(models.Model):

    total_visitors = models.IntegerField(default=0)

    mobile_users = models.IntegerField(default=0)

    desktop_users = models.IntegerField(default=0)

    tablet_users = models.IntegerField(default=0)

    organic_traffic = models.IntegerField(default=0)

    social_traffic = models.IntegerField(default=0)

    direct_traffic = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analytics {self.id}"