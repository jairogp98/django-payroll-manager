from rest_framework.views import APIView, Response
from apps.users.models import User
from apps.users.api.serializers import UserListSerializer, UserCreateSerializer, UserUpdateSerializer, UserChangePasswordSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class UserAPIView(APIView):

    @swagger_auto_schema(responses={200: UserListSerializer(many=True)})
    def get(self, request):
        try:
            users = User.objects.filter(is_active= True)
            users_serialized = UserListSerializer(users, many = True)
            return Response(users_serialized.data, status.HTTP_200_OK)
        except Exception as e:
                return Response (f"ERROR: {e}", 500)

    @swagger_auto_schema(responses={200: UserListSerializer(many=True)}, request_body=UserCreateSerializer)
    def post(self, request):
        try:
            serializer = UserCreateSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        except Exception as e:
                return Response (f"ERROR: {e}", 500)

class UserByIdAPIView(APIView):

    @swagger_auto_schema(responses={200: UserListSerializer(many=True)})
    def get(self,request, pk:int):
        try:
            if pk is None:
                return Response({"message": "You must specify user's id"}, status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.filter(id = pk).first()
                if user is None:
                    return Response({"message": "User not found"}, status.HTTP_404_NOT_FOUND)
                else:
                    user_serialized = UserListSerializer(user)
                    return Response(user_serialized.data, status.HTTP_200_OK)
        except Exception as e:
                return Response (f"ERROR: {e}", 500)

    @swagger_auto_schema(responses={200: UserListSerializer(many=True)}, request_body=UserUpdateSerializer)
    def put (self, request, pk:int):
        try:
            if pk is None:
                return Response({"message": "You must specify user's id"}, status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.filter(id = pk).first()
                if user is None:
                    return Response({"message": "User not found"}, status.HTTP_404_NOT_FOUND)
                else:
                    user_serialized = UserUpdateSerializer(user, data = request.data)
                    if user_serialized.is_valid():
                        user_serialized.save()

                        user_updated = User.objects.filter(id = pk).first()
                        user_updated = UserListSerializer(user_updated)
                        return Response(user_updated.data, status.HTTP_200_OK)
                    else:
                        return Response(user_serialized.errors)
        except Exception as e:
            return Response (f"ERROR: {e}", 500)

    @swagger_auto_schema(responses={200: "Password succesfully updated!"}, request_body= UserChangePasswordSerializer)
    def patch(self, request, pk:int):
        """EP for change user's password"""
        try:
            if pk is None:
                return Response({"message": "You must specify user's id"}, status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.filter(id = pk).first()
                if user is None:
                    return Response({"message": "User not found"}, status.HTTP_404_NOT_FOUND)
                else:
                        password_serialized = UserChangePasswordSerializer(user, data = request.data)
                        if password_serialized.is_valid():
                            user.set_password(request.data['password'])
                            user.save()
                            return Response({'message': 'Password succesfully updated!'}, status.HTTP_200_OK)
                        else:
                            return Response(password_serialized.errors)
        except Exception as e:
                return Response (f"ERROR: {e}", 500)

    @swagger_auto_schema(responses={200: "User -user- deactivated."})
    def delete(self, request, pk:int):
        try:
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
        except Exception as e:
                return Response (f"ERROR: {e}", 500)