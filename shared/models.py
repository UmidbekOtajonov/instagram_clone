from django.db import models
import uuid

class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True



