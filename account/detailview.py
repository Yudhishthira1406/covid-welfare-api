from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import DetailSerializer, SeekSerializer

class DetailView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = DetailSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, slug):
        try:
            user = User.objects.get(username = slug)
        except User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
        serializer = DetailSerializer(user)

        return Response(serializer.data)

    def post(self, request, slug):
        try:
            user = User.objects.get(username = slug)
        except User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        user1 = request.user
        if user1 != user:
            return Response(status = status.HTTP_403_FORBIDDEN)

        serializer = DetailSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            x = serializer.data
            x['email'] = user.email
            return Response(x)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def get_seek(self, request, slug):
        try:
            user = User.objects.get(username = slug)
        except User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        return Response({'seek_text': user.seek_text, 'seek_time':user.seek_time})

    def post_seek(self, request, slug):
        try:
            user = User.objects.get(username = slug)
        except User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        user1 = request.user
        if user1 != user:
            return Response(status = status.HTTP_403_FORBIDDEN)

        serializer = SeekSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'seek_text': user.seek_text, 'seek_time':user.seek_time})

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def seek_list(self, request, slug):
        try:
            user = User.objects.get(username = slug)
        except User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        user1 = request.user
        if user1 != user:
            return Response(status = status.HTTP_403_FORBIDDEN)

        data = []
        query = User.objects.all()
        for user2 in query:
            if user2 != user and user2.provide == True and abs(user.lat - user.lat) <= 1.0 and abs(user.lon - user2.lon) <= 1.0:
                data.append({'username':user2.username, 'lat':user2.lat, 'lon':user2.lon})

        return Response({'data':data})
