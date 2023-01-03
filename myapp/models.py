from django.db import models


class Comment(models.Model):
    comment = models.TextField(blank=False, max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        truncated_text = (
            self.comment if len(self.comment) < 20 else f"{self.comment[:17]}..."
        )
        return f"<{self.id}>: {truncated_text}"
