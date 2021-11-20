from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from blog.models import Post, Category, Comment
from core import urls


class TestCreatePost(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser', password='12345'
        )
        test_category = Category.objects.create(name='test category')
        test_post = Post.objects.create(
            title='test post', content='test content', author=test_user, category=test_category
        )

    def test_blog_content(self):
        post = Post.objects.get(id=1)
        category = Category.objects.get(id=1)
        expected_title = f'{post.title}'
        expected_content = f'{post.content}'
        expected_author = f'{post.author}'
        expected_category = f'{category.name}'

        self.assertEquals(expected_title, 'test post')
        self.assertEquals(expected_content, 'test content')
        self.assertEquals(expected_author, 'testuser')
        self.assertEquals(expected_category, 'test category')
        self.assertEquals(str(post), 'test post')


class TestCreateCategory(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_category = Category.objects.create(name='test category')

    def test_blog_content(self):
        category = Category.objects.get(id=1)
        self.assertEquals(str(category), 'test category')


class TestCreateComment(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username='testuser', password='12345'
        )
        test_category = Category.objects.create(name='test category')
        test_post = Post.objects.create(
            title='test post', content='test content', author=test_user, category=test_category
        )
        test_comment = Comment.objects.create(
            post=test_post,
            name='test name',
            body='test comment'
        )

    def test_blog_content(self):
        comment = Comment.objects.get(id=1)
        expected_body = f'{comment.body}'
        self.assertEquals(expected_body, 'test comment')
        self.assertEquals(str(comment), f'Comment by test name on test post')


class PostTests(APITestCase):
    def test_view_posts(self):
        url = reverse('blog:postlist')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        self.test_category = Category.objects.create(name='test category')
        self.test_user = User.objects.create_user(
            username='testuser', password='12345'
        )

        url = reverse('blog:postlist')
        data = {
            'author': 1,
            'title': 'test post',
            'slug': 'test-post',
            'content': 'test content',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
