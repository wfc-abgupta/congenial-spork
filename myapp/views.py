from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from myapp.models import Comment
from myapp.serializers import CommentSerializer


def frontpage(request):
    return render(request, "frontpage.html")


class CommentListView(ListCreateAPIView):
    """
    Retrieve a list of Comment objects or create a new one
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an existing Comment
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
