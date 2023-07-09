from django.db import models


class BasicModel(models.Model):
    """Abstract base model for basic fields"""

    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
