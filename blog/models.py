from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from .managers import PublishedManager

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published')
)


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        ordering = ('-published',)

    objects = models.Manager()
    published = PublishedManager()

    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='blog_posts'
    )
    content = RichTextField(blank=True, null=True)
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:get_post', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=8)
    email = models.EmailField()
    body = RichTextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


# class BlogImage(models.Model):
#     title = models.CharField(max_length=15)
#     image = FileBrowseField(
#         "Image", max_length=200, directory="blog_images/", extensions=[".jpg"], blank=True)
