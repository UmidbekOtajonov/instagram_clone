from django.urls import path
from .views import PostListAPIView, PostCreateAPIView, PostRetrieveUpdateDestroyAPIView, PostCommentListView, \
    PostCommentCreateView, CommentsListCreateAPIView, PostLikeListView, CommentRetrieveView, CommentLikeListView,\
    PostLikeApiView, CommentLikeApiView

urlpatterns = [
    path( 'list/', PostListAPIView.as_view()),
    path('create/', PostCreateAPIView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('<uuid:pk>/likes/', PostLikeListView.as_view()),
    path('<uuid:pk>/comments/', PostCommentListView.as_view()),
    path('<uuid:pk>/comments/create/', PostCommentCreateView.as_view()),
    path('comments/', CommentsListCreateAPIView.as_view()),
    path('comments/<uuid:pk>/', CommentRetrieveView.as_view()),
    path('comments/<uuid:pk>/likes/', CommentLikeListView.as_view()),
    path('<uuid:pk>/create-delete-like/', PostLikeApiView.as_view()),
    path('<uuid:pk>/comment-create-delete-like/', CommentLikeApiView.as_view()),
]
