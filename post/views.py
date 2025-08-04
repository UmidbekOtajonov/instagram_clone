from http import HTTPStatus
from tokenize import Comment

from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.custom_pagination import CustomPagination
from .models import Post, PostLike, PostComment, CommentLike
from .serializers import PostSerializer, PostLikeSerializer, CommentSerializer, CommentLikeSerializer

class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]


    def put(self,request,*args,**kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "code": HTTPStatus.OK,
                "message": "post updated successfully",
                "data": serializer.data,
            }
        )

    def delate(self,request,*args,**kwargs):
        post = self.get_object()
        post.delate()
        return Response(
            {
                "success": True,
                "code": status.HTTP_204_NO_CONTENT,
                "message": "post deleted successfully",
            }
        )

class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post_id=post_id)
        return queryset


class PostCommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)


class CommentsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = CustomPagination
    queryset = PostComment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieveView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, ]
    queryset = PostComment.objects.all()

class PostLikeListView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [AllowAny, ]


    def get_queryset(self):
        post_id = self.kwargs['pk']
        return PostLike.objects.filter(post_id=post_id)


class CommentLikeListView(generics.ListAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        return CommentLike.objects.filter(comment_id=comment_id)

class PostLikeApiView(APIView):

    def post(self, request, pk ):
        try:
            post_like = PostLike.objects.get(
                author=request.user,
                post_id=pk,
            )
            post_like.delete()
            data = {
                "success": True,
                "message": "post like deleted successfully",
                "data": None
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except PostLike.DoesNotExist:
            post_like = PostLike.objects.create(
                author=request.user,
                post_id=pk,
            )
            serializer = PostLikeSerializer(post_like)
            data = {
                "success": True,
                "message": "post like created successfully",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)


    # def post(self, request, pk):
    #     try:
    #         post_like = PostLike.objects.create(
    #             author = request.user,
    #             post_id = pk
    #         )
    #         serializer = PostLikeSerializer(post_like)
    #         data = {
    #             "success": True,
    #             "message": "post liked successfully",
    #             "data": serializer.data,
    #         }
    #         return Response(data, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         data = {
    #             "success": False,
    #             "message": f"{str(e)}",
    #             "data": None
    #         }
    #         return Response(data, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self,request,pk):
    #     try:
    #         post_like = PostLike.objects.get(
    #             author = request.user,
    #             post_id = pk
    #         )
    #         post_like.delete()
    #         data = {
    #             "success": True,
    #             "message": "post like deleted successfully",
    #             "data": None
    #         }
    #         return Response(data, status=status.HTTP_204_NO_CONTENT)
    #     except Exception as e:
    #         data = {
    #             "success": False,
    #             "message": f"{str(e)}",
    #             "data": None
    #         }
    #         return Response(data, status=status.HTTP_400_BAD_REQUEST)

class CommentLikeApiView(APIView):

    def post(self, request, pk ):
        comment = get_object_or_404(PostComment, id=pk)  # commentni id sini olish kerak
        try:
            comment_like = CommentLike.objects.get(
                comment = comment,
                author=request.user,
            )
            comment_like.delete()
            data = {
                "success": True,
                "message": "comment like deleted successfully",
                "data": None
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExist:
            comment_like = CommentLike.objects.create(
                comment = comment,
                author=request.user,
            )
            serializer = CommentLikeSerializer(comment_like)
            data = {
                "success": True,
                "message": "comment like created successfully",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)



    # def post(self,request,pk):
    #     try:
    #         comment_like = CommentLike.objects.get(
    #             author = request.user,
    #             comment_id = pk
    #         )
    #         serializer = CommentLikeSerializer(comment_like)
    #         data = {
    #             "success": True,
    #             "message": "comment liked successfully",
    #             "data": serializer.data,
    #         }
    #         return Response(data, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         data = {
    #             "success": False,
    #             "message": f"{str(e)}",
    #             "data": None
    #         }
    #         return Response(data, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk):
    #     try:
    #         comment_like = CommentLike.objects.get(
    #             author = request.user,
    #             comment_id = pk
    #         )
    #         comment_like.delete()
    #         data = {
    #             "success": True,
    #             "message": "comment like deleted successfully",
    #             "data": None
    #         }
    #         return Response(data, status=status.HTTP_204_NO_CONTENT)
    #     except Exception as e:
    #         data = {
    #             "success": False,
    #             "message": f"{str(e)}",
    #             "data": None
    #         }
    #         return Response(data, status=status.HTTP_400_BAD_REQUEST)



