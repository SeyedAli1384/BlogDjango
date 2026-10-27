from django.core.cache import cache
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import BlogForm
from .models import Blog, Comments, Topic

@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "blog-test-cache",
        }
    }
)
class BlogTestBase(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(
            username="author",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            username="another",
            password="StrongPass456!",
        )
        self.topic = Topic.objects.create(name="Python")
        self.blog = Blog.objects.create(
            topic=self.topic,
            author=self.user,
            title="Test Blog",
            blog="This is test content.",
        )

@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "blog-test-cache",
        }
    }
)
class PublicPageTests(BlogTestBase):
    def test_home_page_returns_200(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Blog")

    def test_about_page_returns_200(self):
        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)

    def test_blog_detail_returns_200(self):
        response = self.client.get(
            reverse("blog", args=[self.blog.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Blog")

    def test_profile_page_returns_200(self):
        response = self.client.get(
            reverse("profile", args=[self.user.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_search_filters_blogs(self):
        response = self.client.get(
            reverse("home"), {"q": "nonexistent-title"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Blog")
    
    def test_home_cache_refreshes_after_blog_creation(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Test Blog")
    
        new_blog = Blog.objects.create(
            topic=self.topic,
            author=self.user,
            title="New Cached Blog",
            blog="This blog was created after the cache was populated.",
        )
    
        response = self.client.get(reverse("home"))
        self.assertContains(response, "New Cached Blog")

@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "blog-test-cache",
        }
    }
)
class AuthenticationTests(BlogTestBase):
    def test_login_page_returns_200(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "author",
                "password": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("home"))

    def test_authenticated_user_can_logout(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("logout"))

        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_register_page_returns_200(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)

@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "blog-test-cache",
        }
    }
)
class BlogMutationTests(BlogTestBase):
    def test_anonymous_user_is_redirected_from_create(self):
        response = self.client.get(reverse("create-blog"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_authenticated_user_can_create_blog(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("create-blog"),
            {
                "title": "New Blog",
                "blog": "Created through a test.",
                "topic": self.topic.pk,
            },
        )

        self.assertRedirects(response, reverse("home"))

        created_blog = Blog.objects.get(title="New Blog")
        self.assertEqual(created_blog.author, self.other_user)

    def test_author_can_update_blog(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("update-blog", args=[self.blog.pk]),
            {
                "title": "Updated Blog",
                "blog": "Updated content.",
                "topic": self.topic.pk,
                "author": self.user.pk,
            },
        )

        self.assertRedirects(response, reverse("home"))

        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, "Updated Blog")

    def test_other_user_cannot_update_blog(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("update-blog", args=[self.blog.pk]),
            {
                "title": "Hijacked Blog",
                "blog": "Unauthorized change.",
                "topic": self.topic.pk,
            },
        )

        self.assertRedirects(response, reverse("home"))

        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, "Test Blog")

    def test_other_user_cannot_delete_blog(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("delete-blog", args=[self.blog.pk])
        )

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(Blog.objects.filter(pk=self.blog.pk).exists())

    def test_author_can_delete_blog(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("delete-blog", args=[self.blog.pk])
        )

        self.assertRedirects(response, reverse("home"))
        self.assertFalse(Blog.objects.filter(pk=self.blog.pk).exists())

@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "blog-test-cache",
        }
    }
)
class CommentTests(BlogTestBase):
    def test_comment_is_created_for_authenticated_user(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("blog", args=[self.blog.pk]),
            {"body": "A test comment"},
        )

        self.assertRedirects(
            response, reverse("blog", args=[self.blog.pk])
        )
        self.assertTrue(
            Comments.objects.filter(
                blog=self.blog,
                user=self.other_user,
                body="A test comment",
            ).exists()
        )


class BlogFormSecurityTests(TestCase):
    def test_author_is_not_editable_through_blog_form(self):
        self.assertNotIn("author", BlogForm().fields)

    def test_participants_are_not_editable_through_blog_form(self):
        self.assertNotIn("Participants", BlogForm().fields)