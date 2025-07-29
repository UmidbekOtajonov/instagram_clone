from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Post, PostLike, PostComment, CommentLike
from .serializers import PostSerializer, PostLikeSerializer, CommentSerializer, CommentLikeSerializer

class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return Post.objects.all()

