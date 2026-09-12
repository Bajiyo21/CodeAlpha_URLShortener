from django.db import models


class UrlMapping(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.short_code} -> {self.original_url}'
