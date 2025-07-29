from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

from shared.models import BaseModel



User = get_user_model()

class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    caption = models.TextField(validators=[MaxLengthValidator(2000)])

    class Meta:
        db_table = 'posts'
        verbose_name_plural = 'posts'
        verbose_name = 'post'

    def __str__(self):
        return f"{self.author} post about {self.caption}"


class PostComment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child',
        blank=True,
        null=True
    )
    def __str__(self):
        return f"comment by {self.author}"


class PostLike(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'post'],
                name='PostLike_unique'
            )
        ]

class CommentLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'comment'],
                name='CommentLike_unique'
            )
        ]

