from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GroupSerialize


@api_view()
def trie_story_view(request: Request) -> Response:
    return Response({'message': 'Everything is Good'})


# class GroupListView(APIView):
#     def get(self, request: Request) -> Response:
#         groups = Group.objects.all()
#         groups_details = GroupSerialize(groups, many=True)
#         return Response({'groups': groups_details.data})

# class GroupListView(ListModelMixin, APIView):
#     queryset = Group.objects.all()
#     serialized_class = GroupSerialize
#     def get(self, request: Request) -> Response:
#         return self.list(request)
class GroupListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerialize
