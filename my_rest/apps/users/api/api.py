from rest_framework.views import APIView, Response
from apps.users.models import User
from apps.users.api.serializers import UserSerializer
from rest_framework import status

class UserAPIView(APIView):

    def get(self, request):

       users = User.objects.filter(is_active= True)
       users_serialized = UserSerializer(users, many = True)
       return Response(users_serialized.data, status.HTTP_200_OK)

    def post(self, request):

        serializer = UserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class UserAPIViewById(APIView):

    def get(self,request, pk):

        if pk is None:
            return Response({"message": "You must specify user's id"}, status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.filter(id = pk).first()
            if user is None:
                return Response({"message": "User not found"}, status.HTTP_404_NOT_FOUND)
            else:
                user_serialized = UserSerializer(user)
                return Response(user_serialized.data, status.HTTP_200_OK)

    def put (self, request, pk):
        if pk is None:
            return Response({"message": "You must specify user's id"}, status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.filter(id = pk).first()
            if user is None:
                return Response({"message": "User not found"}, status.HTTP_404_NOT_FOUND)
            else:
                user_serialized = UserSerializer(user, data = request.data)
                if user_serialized.is_valid():
                    user_serialized.save()
                    return Response(user_serialized.data, status.HTTP_200_OK)
                else:
                    return Response(user_serialized.errors)

    def patch(self, request, pk):
        if pk is None:
            return Response({"message": "You must specify user's id"}, status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.filter(id = pk).first()
            if user is None:
                return Response({"message": "User not found"}, status.HTTP_404_NOT_FOUND)
            else:
                    user.set_password(request.data['password'])
                    user.save()
                    return Response({'message': 'Password succesfully changed!'}, status.HTTP_200_OK)

    def delete(self, request, pk):
        if pk is None:
            return Response({'message':"You must specify user's id"}, status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.filter(id = pk).first()
            if user is None:
                return Response({"message": "User not found"}, status.HTTP_404_NOT_FOUND)
            else:
                    user.is_active = False
                    user.save()
                    return Response({f'message': 'User {user.email} deactivated.'}, status.HTTP_200_OK)