from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post


class PostAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="Melissa",
            password="testpassword123"
        )

        self.other_user = User.objects.create_user(
            username="John",
            password="testpassword123"
        )

        self.client.force_authenticate(user=self.user)

        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=self.user
        )

    def test_create_post(self):
        data = {
            "title": "New Post",
            "content": "Testing post creation."
        }

        response = self.client.post(
            "/api/posts/",
            data,
            format="json",
            HTTP_IDEMPOTENCY_KEY="test-create-001"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], "Melissa")

    def test_list_posts(self):
        response = self.client.get("/api/posts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_post(self):
        response = self.client.get(f"/api/posts/{self.post.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_can_update_post(self):
        data = {"title": "Updated Title"}

        response = self.client.patch(
            f"/api/posts/{self.post.id}/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_update_post(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.patch(
            f"/api/posts/{self.post.id}/",
            {"title": "Unauthorized Update"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_delete_post(self):
        response = self.client.delete(f"/api/posts/{self.post.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_other_user_cannot_delete_post(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(f"/api/posts/{self.post.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_missing_post_returns_404(self):
        response = self.client.get("/api/posts/9999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)