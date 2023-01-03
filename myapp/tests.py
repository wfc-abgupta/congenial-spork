from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import json

from myapp.models import Comment
from myapp.serializers import CommentSerializer


class CommentListTestViewTestCase(TestCase):
    def setUp(self):
        self.comments = [
            Comment.objects.create(comment="Test Comment 1"),
            Comment.objects.create(comment="Test Comment 2"),
        ]
        self.base_url = reverse("comments_list")

    def test_get_comment_list(self):
        response = self.client.get(self.base_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = json.loads(response.content)
        self.assertEqual(len(content), len(self.comments))

        expected_comment_ids = [comment.id for comment in self.comments]
        actual_comment_ids = [comment.get("id") for comment in content]
        self.assertEqual(expected_comment_ids, actual_comment_ids)

    def test_get_returns_expected_fields(self):
        response = self.client.get(self.base_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_content = [
            {
                "id": comment.id,
                "comment": comment.comment,
                "created": comment.created.isoformat().replace("+00:00", "Z"),
            }
            for comment in self.comments
        ]
        content = json.loads(response.content)
        self.assertEqual(content, expected_content)

    def test_get_returns_empty_list_if_no_comments(self):
        Comment.objects.all().delete()
        self.assertEqual(Comment.objects.count(), 0)

        response = self.client.get(self.base_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = json.loads(response.content)
        self.assertIsInstance(content, list)
        self.assertEqual(len(content), 0)

    def test_create_comment(self):
        original_comment_count = Comment.objects.count()

        new_comment_post_data = {"comment": "Another comment"}

        response = self.client.post(
            self.base_url, new_comment_post_data, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        content = json.loads(response.content)
        self.assertEqual(new_comment_post_data.get("comment"), content.get("comment"))

        # Should be one new comment
        new_comment_count = Comment.objects.count()
        self.assertEqual(original_comment_count + 1, new_comment_count)

    def test_error_on_creation_if_no_comment(self):
        original_comment_count = Comment.objects.count()

        new_comment_post_data = {"comment": ""}

        response = self.client.post(
            self.base_url, new_comment_post_data, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # No comment should have been created
        new_comment_count = Comment.objects.count()
        self.assertEqual(original_comment_count, new_comment_count)


class CommentDetailViewTestCase(TestCase):
    def setUp(self):
        self.comment = Comment.objects.create(comment="Test Comment 1")
        self.get_base_url_for_pk = lambda pk: reverse(
            "comment_detail", kwargs={"pk": pk}
        )

    def test_get_comment(self):
        base_url = self.get_base_url_for_pk(self.comment.pk)
        response = self.client.get(base_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        content = json.loads(response.content)
        self.assertIsInstance(content, dict)
        self.assertEqual(content["id"], self.comment.id)

    def test_get_404_if_comment_pk_does_not_exist(self):
        nonexistant_pk = Comment.objects.order_by("pk").last().pk + 1
        self.assertFalse(Comment.objects.filter(pk=nonexistant_pk).exists())

        base_url = self.get_base_url_for_pk(nonexistant_pk)
        response = self.client.get(base_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_existing_comment(self):
        original_comment = self.comment.comment

        new_comment = f"{original_comment} with added extra text"
        put_body = {"comment": new_comment}

        base_url = self.get_base_url_for_pk(self.comment.pk)
        response = self.client.put(
            base_url, put_body, format="json", content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.comment.refresh_from_db()
        self.assertEqual(self.comment.comment, new_comment)

    def test_put_400_if_no_comment_on_update(self):
        new_comment = ""
        put_body = {"comment": new_comment}

        base_url = self.get_base_url_for_pk(self.comment.pk)
        response = self.client.put(
            base_url, put_body, format="json", content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_404_if_comment_pk_does_not_exist(self):
        nonexistant_pk = Comment.objects.order_by("pk").last().pk + 1
        self.assertFalse(Comment.objects.filter(pk=nonexistant_pk).exists())

        base_url = self.get_base_url_for_pk(nonexistant_pk)
        response = self.client.get(base_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_created_timestamp_does_not_save_on_update(self):
        original_timestamp = self.comment.created
        original_comment = self.comment.comment

        new_comment = f"{original_comment} with added extra text"
        put_body = {"comment": new_comment}

        base_url = self.get_base_url_for_pk(self.comment.pk)
        response = self.client.put(
            base_url, put_body, format="json", content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.comment.refresh_from_db()
        # Show that Comment object was updated
        self.assertEqual(self.comment.comment, new_comment)
        # Show that Comment created timestamp was not updated
        self.assertEqual(self.comment.created, original_timestamp)

    def test_delete_comment(self):
        original_comment_count = Comment.objects.count()

        base_url = self.get_base_url_for_pk(self.comment.pk)
        response = self.client.delete(base_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        new_comment_count = Comment.objects.count()
        self.assertEqual(original_comment_count - 1, new_comment_count)

    def test_cannot_delete_nonexistant_comment(self):
        nonexistant_pk = Comment.objects.order_by("pk").last().pk + 1
        self.assertFalse(Comment.objects.filter(pk=nonexistant_pk).exists())

        base_url = self.get_base_url_for_pk(nonexistant_pk)
        response = self.client.delete(base_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
